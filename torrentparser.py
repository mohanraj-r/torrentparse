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
        
        self.torrent_content = open(torrent_file_path, 'r').read()
        
    
    def __str__(self):
        #TODO
        pass
    
    
    def get_tracker_url(self):
        ''' Parses torrent content and returns the tracker URL '''
        pass
    
    
    def get_creation_date(self):
        ''' Parses torrent content and returns creation date of the torrent'''
        match = re.findall('13:creation datei(?P<creation_date>[0-9]+)e', self.torrent_content)
        if not match:   
            return None
        else:
            assert len(match) == 1, 'Something is amiss. Multiple creation dates found in torrent file.'
            return int(match[0])        
    
    
    def get_client_name(self):
        pass
    
    
    def get_files_details(self):
        pass
    
    def _parse_int(self):
        pass
        