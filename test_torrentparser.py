'''
Created on 2012-03-07

@author: mohanr

TODOs:
    . Use of multiple assertions inside a single test case seems not a clean way of doing it. Investigate and fix.
    . Use of for loops inside test cases seems smelly. Investigate and fix.

'''
from datetime import datetime
import unittest

from torrentparser import TorrentParser
from test_data.data_torrents_info import TORRENTS_INFO

class TestTorrentParse(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_parsercreation_invalidtype_file_input(self):
        ''' Test invalid inputs while creating parser object. '''
        self.assertRaises(ValueError, TorrentParser, None)
        self.assertRaises(ValueError, TorrentParser, 123)

    def test_parsercreation_nonexistent_file_input(self):
        ''' Test non-existent file paths. '''
        self.assertRaises(IOError, TorrentParser, '')
        self.assertRaises(IOError, TorrentParser, 'I:/nvalid/file/path')

    def test_get_tracker_url(self):
        ''' Test getting Tracker URL from a valid torrent file. '''
        for torrent_file in TORRENTS_INFO:
            tp = TorrentParser('test_data/%s' % torrent_file)
            self.assertEqual(tp.get_tracker_url(), TORRENTS_INFO[torrent_file]['tracker_url']) 

    def test_get_creation_date(self):
        ''' Test getting creation date from a valid torrent file. ''' 
        for torrent_file in TORRENTS_INFO:
            tp = TorrentParser('test_data/%s' % torrent_file)
            self.assertEqual(tp.get_creation_date(), 
                             datetime.utcfromtimestamp(TORRENTS_INFO[torrent_file]['creation_date']).isoformat())

    def test_get_client_name(self):
        ''' Test getting Client name from a valid torrent file. '''          
        for torrent_file in TORRENTS_INFO:
            tp = TorrentParser('test_data/%s' % torrent_file)
            self.assertEqual(tp.get_client_name(), TORRENTS_INFO[torrent_file]['client_name'])

    def test_get_files_details(self):
        ''' Test getting the name, length and checksum of the files inside a valid torrent file. '''
        for torrent_file in TORRENTS_INFO:
            tp = TorrentParser('test_data/%s' % torrent_file)
            self.assertItemsEqual(tp.get_files_details(), TORRENTS_INFO[torrent_file]['file_details']) 

if __name__ == "__main__":    
    unittest.main()
    