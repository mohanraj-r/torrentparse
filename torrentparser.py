'''
Parses a torrent file and provides method to access the following attributes.
    . Tracker URL
    . Creation date
    . Client name, if any
    . For each file
        . name
        . length
        . checksum

Created on 2012-03-07

@author: mohanr
'''

from datetime import datetime
import os
import re
import string
import types


class ParsingError(Exception):
    ''' Error class representing errors that occur while parsing the torrent content. '''
    def __init__(self, error_msg):
        self.error_msg = error_msg
    
    def __str__(self):
        return repr(self.error_msg) 


class TorrentParser(object):
    '''
    Parses a torrent file and returns various properties based on the content of the torrent file.
    '''
    INT_START = 'i'
    DICT_START = 'd'
    LIST_START = 'l'
    INT_DICT_LIST_END = 'e'
    STR_LEN_VALUE_SEP = DICT_KEY_VALUE_SEP = ':'
       

    def __init__(self, torrent_file_path):
        '''
        Reads the torrent file and sets the content as an object attribute.
        
        Args:
            torrent_file_path - String containing path to the torrent file to be parsed
        Returns:
            None
        Raises:
            ValueError - when passed arg is not of string type
            IOError - when the string arg passed points to a non-existent file
                    
        '''
        if not isinstance(torrent_file_path, types.StringType): 
            raise ValueError('Path of the torrent file expected in string format.')
        
        if not os.path.exists(torrent_file_path):
            raise IOError("No file found at '%s'" % torrent_file_path)
        
        self.torrent_file = open(torrent_file_path, 'r')
        self.torrent_content = self.torrent_file.read()
        
        self.parsed_content = ''
        self._parse_mode = [] # Stack to keep track of the parsing mode
        self.generator_index = 0
  
    
    def get_tracker_url(self):
        ''' Parses torrent file and returns the tracker URL '''
        match = re.findall('d8:announce(?P<tracker_len>[0-9]+):', self.torrent_content)
        tracker_url_len = int(match[0])
        self.torrent_file.seek(len('d8:announce%d:' %tracker_url_len))
        return self.torrent_file.read(tracker_url_len)

    
    def get_creation_date(self):
        ''' Parses torrent file and returns creation date of the torrent, if present, in ISO format '''
        match = re.findall('13:creation datei(?P<creation_date>[0-9]+)e', self.torrent_content)
        creation_date = None
        
        if match:
            assert len(match) == 1, 'Something is amiss. More than one creation date found in torrent file.'
            creation_date = datetime.utcfromtimestamp(int(match[0]))
            creation_date = creation_date.isoformat()
        
        return creation_date         
            
    
    def get_client_name(self):
        ''' Parses torrent file and returns the name of the client that created the torrent if present '''
        match = re.search('10:created by(?P<client_len>[0-9]+):', self.torrent_content)
        client_name = None
        
        if match:
            match_dict = match.groupdict()
            assert len(match_dict) == 1, 'Something is amiss. More than one client name found in torrent file.'
            client_name_len = int(match_dict['client_len'])            
            self.torrent_file.seek(match.end())
            client_name = self.torrent_file.read(client_name_len)
        
        return client_name

    
    def get_files_details(self):
        ''' Parses torrent file and returns details of the files contained in the torrent. 
            Details include name, length and checksum for each file in the torrent.
        '''
        # Pattern to match file information in Single file torrents
        match = re.search('4:infod6:lengthi(?P<file_length>[0-9]+)e4:name(?P<file_name_len>[0-9]+):', self.torrent_content)
        file_name = file_length = None
        file_details = ()
        
        if match:
            match_dict = match.groupdict()
            assert len(match_dict) == 2, 'Unable to match torrent file details inside torrent file.'
            file_name_len = int(match_dict['file_name_len'])
            self.torrent_file.seek(match.end())
            file_name = self.torrent_file.read(file_name_len)
            file_length = int(match_dict['file_name_len'])
            file_details = (file_name, file_length, ) 
            
        return file_details
    
    
    def _parse_torrent(self):
        ''' Parse the torrent content in bencode format into python data format. '''        
        str_len = ''
        for cur_char in self._iter_torrent_content():
            print cur_char # DEBUG                 
            if cur_char in string.digits and self._parse_mode != 'INT': 
                if self._parse_mode[-1] != 'STR_LEN':
                    self._parse_mode.append('STR_LEN')
                    self.parsed_content += "'"
                str_len += cur_char
                continue
            elif cur_char == self.DICT_START:
                self._parse_mode.append('DICT')
                self._parse_mode.append('DICT_KEY')
                self.parsed_content += "{"
                continue
            elif cur_char == self.LIST_START:
                self._parse_mode.append('LIST')
                self.parsed_content = "["
                continue
            elif cur_char == self.INT_START:
                self._parse_mode.append('INT')
                continue
            elif cur_char == self.INT_DICT_LIST_END:
                self._parse_mode.pop()
                close_struct = self._parse_mode.pop()
                if close_struct == 'DICT':
                    self.parsed_content[-1] = "}" # Overwrite the comma inserted for next dict key.    
                elif close_struct == 'LIST':
                    self.parsed_content += "]"
                                
                continue                        
                   
            # Parse string of format: <str_len>:string
            if (self._parse_mode[-1] == 'STR_LEN' or self._parse_mode[-1] == 'DICT_KEY' or 
                self._parse_mode[-1] == 'DICT_VALUE'):
                if cur_char in string.digits:
                    str_len += cur_char
                elif cur_char == self.STR_LEN_VALUE_SEP:
                    print 'str len %s ' % str_len # DEBUG
                    # Parse str of len str_len
                    torr_iter = self._iter_torrent_content()
                    torr_iter.next()
                    for _ in range(int(str_len)):
                        self.parsed_content += torr_iter.next()
                    self.parsed_content += "'" # close string quote
                    self._parse_mode.pop()
                    str_len = ''
                    
                    if self._parse_mode[-1] == 'DICT_KEY':
                        self._parse_mode.pop()
                        self._parse_mode.append('DICT_VALUE') 
                        self.parsed_content += ':'
#                    if self._parse_mode[-1] == 'DICT' or self._parse_mode[-1] == 'LIST':
                    elif self._parse_mode[-1]  == 'DICT_VALUE':
                        self._parse_mode.pop()
                        self._parse_mode.append('DICT_KEY')                         
                        self.parsed_content += ','
                    
                else:
                    raise ParsingError('Error while parsing a String. Parser at position %d.' % len(self.parsed_content))
                
                continue
                 
            elif self._parse_mode[-1] == 'INT':
                while True:
                    cur_char = self._iter_torrent_content()
                    
                    if cur_char == self.INT_DICT_LIST_END:                        
                        self._parse_mode.pop()
                        
#                        if self._parse_mode[-1] == 'DICT' or self._parse_mode[-1] == 'LIST':
#                            self.parsed_content += ','
                        if self._parse_mode[-1]  == 'DICT_VALUE':
                            self._parse_mode.pop()
                            self._parse_mode.append('DICT_KEY')                         
                            self.parsed_content += ','

                        
                        break
                    elif cur_char in string.digits:
                        self.parsed_content += cur_char
                    else:
                        raise ParsingError('Error while parsing an integer. Parser at position %d.' % len(self.parsed_content))
                                    
                continue
            
            elif self._parse_mode[-1] == 'DICT':
                self._parse_mode.append('DICT_KEY') # Parse dict key
                continue                                          
                 
    
    def _iter_torrent_content(self):
        ''' Generator function that helps iterate over the content of the torrent file, single character at a time. '''        
        while self.generator_index < len(self.torrent_content):
            yield(self.torrent_content[self.generator_index])
            self.generator_index +=1
