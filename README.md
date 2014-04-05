What
====
Parse a torrent file (bdecode) in Python without any 3rd party libraries and provide methods to access the following attributes

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
Resources that I used to understand Torrent file structure:

* http://fileformats.wikia.com/wiki/Torrent_file
* http://wiki.theory.org/BitTorrentSpecification
* http://en.wikipedia.org/wiki/Bencode
* http://en.wikipedia.org/wiki/Torrent_file

Example
=======
The following stream of characters in the torrent file
"d8:announce33:http://jip.cs.vu.nl:6969/announce13:creation datei1147934820e4:infod6:lengthi445866736e4:name24:Elephants_Dream_1024.avi12:piece lengthi262144e6:pieces34020:"

is transformed into
{'creation date': 1147934820, 'announce': 'http://jip.cs.vu.nl:6969/announce', 'info': {'length': 44
5866736, 'piece length': 262144, 'name': 'Elephants_Dream_1024.avi', 'pieces':

The torrentparse python module takes torrent files as command line arguments, parses and prints info.
```
$ python torrentparse.py  ../tests/test_data/wired-creative-commons-cd.torrent
Parsing file ../tests/test_data/wired-creative-commons-cd.torrent
../tests/test_data/wired-creative-commons-cd.torrent
http://www.legaltorrents.com:7070/announce 2004-10-26T04:49:05 None [('01-beasti
e-boys-now-get-busy.mp3', 5848493), ('02-david-byrne-my-fair-lady.mp3', 8484766)
, ('03-zap-mama-wadidyusay.mp3', 8044860), ('04-my-morning-jacket-one-big-holida
y.mp3', 12878571), ('05-spoon-revenge.mp3', 5928936), ('06-gilberto-gil-oslodum.
mp3', 9528615), ('07-dan-the-automator-relaxation-spa-treatment.mp3', 8217290),
('08-thievery-corporation-dc-3000.mp3', 10715627), ('09-le-tigre-fake-french.mp3
', 6917415), ('10-paul-westerberg-looking-up-in-heaven.mp3', 7693791), ('11-chuc
k-d-fine-arts-militia-no-meaning-no.mp3', 7717832), ('12-the-rapture-sister-savi
our-blackstrobe-remix.mp3', 17020560), ('13-cornelius-wataridori-2.mp3', 1720025
9), ('14-danger-mouse-jemini-what-u-sittin-on.mp3', 8329130), ('15-dj-dolores-os
lodum-2004.mp3', 9621615), ('16-matmos-action-at-a-distance.mp3', 6588280), ('wi
red-creative-commons-cd.txt', 3992)]
********************************************************************************
```

It can also take multiple files or glob patterns.
```
$ python torrentparse.py  ../tests/test_data/*.torrent
...
```

If no files are given, it parses the test data files and prints info.
```
$ python torrentparse.py
Parsing test torrent files ..
torrentparse\tests\test_data\Elephants Dream (avi) (1024x576).torrent
http://jip.cs.vu.nl:6969/announce 2006-05-18T06:47:00 None [('Elephants_Dream_1024.avi', 445866736)]
...
```

Existing implementations
========================
* http://pypi.python.org/pypi/BitTorrent-bencode/5.0.8
* http://wiki.theory.org/Decoding_bencoded_data_with_python
* http://effbot.org/zone/bencode.htm
