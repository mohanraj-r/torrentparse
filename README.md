What
====
Parse a torrent file in Python without using any 3rd party libraries and provide methods to access the following attributes 
* tracker url, 
* creation date,
* name of the client that created the torrent, and
* for each file in the torrent
** name, length and checksum of the file (getting checksum is not implemented yet)

Why
===
I was asked to write this as part of an interview process.

How
===
Resources that I used to understand Torrent file structure
* http://fileformats.wikia.com/wiki/Torrent_file
* http://wiki.theory.org/BitTorrentSpecification
* http://en.wikipedia.org/wiki/Bencode
* http://en.wikipedia.org/wiki/Torrent_file

Example
=======
The following stream of characters in the torrent file
> "d8:announce33:http://jip.cs.vu.nl:6969/announce13:creation datei1147934820e4:infod6:lengthi445866736e4:name24:Elephants_Dream_1024.avi12:piece lengthi262144e6:pieces34020:"

is transformed into
> { 'creation date': 1147934820, 
>   'announce': 'http://jip.cs.vu.nl:6969/announce', 
>   'info': { 'length': 445866736, 
>             'piece length': 262144, 
>             'name': 'Elephants_Dream_1024.avi', 
>             'pieces':

Existing implementations
========================
* http://pypi.python.org/pypi/BitTorrent-bencode/5.0.8
* http://wiki.theory.org/Decoding_bencoded_data_with_python
* http://effbot.org/zone/bencode.htm
 