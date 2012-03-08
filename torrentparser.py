'''
Created on 2012-03-07

@author: mohanr
'''


class TorrentParser(object):
    '''
    classdocs
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
        