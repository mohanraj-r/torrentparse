'''
Contains information about the torrents in this directory. Used in testing.

Created with the help of BEncode Editor found at http://forum.utorrent.com/viewtopic.php?id=31306 

Created on 2012-03-07

@author: mohanr
'''

from os.path import sep

TORRENTS_INFO = {
    'Elephants Dream (avi) (1024x576).torrent': { # name of torrent file as in the file system
        'tracker_url': 'http://jip.cs.vu.nl:6969/announce',
        'creation_date': 1147934820,
        'client_name': None,         
        'file_details': (('Elephants_Dream_1024.avi', 445866736, ),) # Tuple of tuples containing (['path','of','file'], 'length', 'checksum') for each file in torrent
    },
                 
    'Honest Man- The Life of R. Budd Dwyer (720p).torrent': {
        'tracker_url': 'http://tracker.vodo.net:6970/announce',
        'creation_date': 1327345573,
        'client_name': None,         
        'file_details': (('An.Honest.Man.720p.x264-VODO.mkv', 1436161730,),
                         ('Sample' + sep + 'An.Honest.Man.720p.x264.Sample-VODO.mkv', 31546414,),
                         ('Show.your.support.now!.URL', 137,),
                         ('vodo.nfo', 6142,),
                         ),                                                                     
    },

    'Megan Lisa Jones - Captive BitTorrent Edition.torrent': { 
        'tracker_url': 'http://tracker001.clearbits.net:7070/announce',
        'creation_date': 1301590654,
        'client_name': 'mktorrent 1.0',         
        'file_details': (('Captive by Megan Lisa Jones - Bittorrent Edition.pdf', 3075568,),
                         ('Description.txt', 1872, ),
                         ('Introduction to Captive by Megan Lisa Jones - BitTorrent Edition.mov', 219561953,),
                         ('License.txt', 142, ),
                         ),
    },
}