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
from StringIO import StringIO
import os
import re
import string
import types


class ParsingError(Exception):
    ''' Error class representing errors that occur while parsing the torrent content. '''
    def __init__(self, error_msg):
        Exception.__init__(self)
        self.error_msg = error_msg        
    
    def __str__(self):
        return repr(self.error_msg) 


class TorrentParser(object):
    '''
    Parses a torrent file and returns various properties based on the content of the torrent file.
    '''
        
    DICT_START = 'd'
    LIST_START = 'l'
    DICT_LIST_END = 'e'
    DICT_KEY_VALUE_SEP = ': '
    DICT_LIST_ITEM_SEP = ', '
    INT_START = 'i'    
    
    class _TorrentStr(object):
        ''' StringIO wrapper over the torrent string. '''
        
        STR_LEN_VALUE_SEP = ':'
        INT_END = 'e'    
        
        def __init__(self, torr_str):
            self.torr_str = StringIO(torr_str)
            self.curr_char = None
        
        def next_char(self):
            self.curr_char = self.torr_str.read(1) # to provide 2 ways of accessing the current parsed char - 1. as return value, 2. as self.curr_char (useful in some circumstances)
            return self.curr_char
        
        def step_back(self, position=-1, mode=1):
            ''' Step back, by default, 1 position relative to the current position. '''
            self.torr_str.seek(-1, 1) 
        
        def parse_str(self):
            ''' Parse and return a string from the torrent file content. Format <string length>:<string>
            
                TODO: 
                    . Explore using regex to accomplish the parsing.            
            '''
#            self.step_back() # since the first digit of the str length would have been already consumed at this point
                        
            str_len = ''
            while True:
                str_len_char = self.next_char()
                if str_len_char not in string.digits:
                    if str_len_char != self.STR_LEN_VALUE_SEP:
                        raise ParsingError('Invalid character %s found after parsing string length (%s expected) at position %d.' % 
                                           (str_len_char, self.STR_LEN_VALUE_SEP, self.torr_str.pos))                     
                    break
                
                str_len += str_len_char 
            
            if not str_len:
                raise ParsingError('Empty string length found while parsing at position %d' % self.torr_str.pos)
            
            return '"' + self.torr_str.read(int(str_len)) + '"'        
            
        def parse_int(self):
            ''' Parse and return an integer from the torrent file content. Format i[0-9]+e
            
                TODO: 
                    . Explore using regex to accomplish the parsing.
                    . Could re-purpose this function to parse str_length.
            '''
            self.step_back() # just to make sure we are parsing the integer of correct format
            
            if self.next_char() != TorrentParser.INT_START:
                raise ParsingError('Error while parsing for an integer. Found %s at position %d while %s is expected.' %
                                   (self.curr_char, self.torr_str.pos, TorrentParser.INT_START))
            
            parsed_int = ''
            while True:
                parsed_int_char = self.next_char()
                if parsed_int_char not in string.digits:
                    if parsed_int_char != self.INT_END:
                        raise ParsingError('Invalid character %s found after parsing an integer (%s expected) at position %d.' % 
                                           (parsed_int_char, self.INT_END, self.torr_str.pos))                     
                    break
                
                parsed_int += parsed_int_char
                
            return int(parsed_int)    
       

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
        
        self.torrent_file = open(torrent_file_path)
        self.torrent_content = self.torrent_file.read()
        self.torrent_str = self._TorrentStr(self.torrent_content)
        
        self.parsed_content = ""
  
    
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
        ''' Parse the torrent content in bencode format into python data format.
        
            Returns:
                A dictionary containing info parsed from torrent file.
        
            TOFIX:
                . The parsing works fine for single file torrents. Multi-file torrents have some problems. FIX.
                . Dict values contain None at times. Shouldn't happen for valid torrent files. FIX.
                . The parsed dict is inside a string. eval(string) throws an error. 
                  Probably due to the hash values (their encoding). Invesitage and FIX.
                        
        '''
        parsed_char = self.torrent_str.next_char()
        
        if not parsed_char: return # EOF
        
        # Parsing logic 
        if parsed_char == self.DICT_LIST_END: 
            return
        
        elif parsed_char == self.INT_START:
            return self.torrent_str.parse_int()
        
        elif parsed_char in string.digits: # string
            self.torrent_str.step_back()
            return self.torrent_str.parse_str()
        
        elif parsed_char == self.DICT_START:
            self.parsed_content += '{' 
            while True:
                dict_key = self._parse_torrent()
                if not dict_key: 
                    break # End of dict
                self.parsed_content += dict_key + self.DICT_KEY_VALUE_SEP
                dict_value = self._parse_torrent() # parse value
#                if dict_value: #DEBUG 
#                    continue
                self.parsed_content += '%s %s' % (dict_value, self.DICT_LIST_ITEM_SEP) #%s coercion needed since key values can be any value. so + concatenation could fail.               
            
            self.parsed_content += '}, '
            return        
        
        elif parsed_char == self.LIST_START:
            self.parsed_content += '['
            while True:
                list_item = self._parse_torrent()
                if not list_item: 
                    break # End of list  
                self.parsed_content +=  list_item + self.DICT_LIST_ITEM_SEP
            
            self.parsed_content += '], '
            return                
        
        #return eval(self.parsed_content) # DEBUG - Throws an error
        return self.parsed_content 
        
if __name__ == '__main__':
    
    test_files = ['test_data/Elephants Dream (avi) (1024x576).torrent', # single file torrent
                  'test_data/Megan Lisa Jones - Captive BitTorrent Edition.torrent', # multi-file torrent
                  'test_data/paz - young broke and fameless_ the mixtape.torrent', # multi-file torrent
                  ]
    for test_file in test_files:
        tp = TorrentParser(test_file)
        print tp._parse_torrent()           