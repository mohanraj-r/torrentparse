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
import types

class TorrentParser(object):
    '''
    Parses a torrent file and returns various properties based on the content of the torrent file.
    '''   

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
        
    
    def __str__(self):
        #TODO
        pass
    
    
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
            client_name_len = match_dict['client_len']            
            self.torrent_file.seek(match.end())
            client_name = self.torrent_file.read(client_name_len)
        
        return client_name
    
    def get_files_details(self):
        pass
    
    def _parse_int(self):
        pass
        