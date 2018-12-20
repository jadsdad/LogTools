from mutagen import flac, mp3
from mutagen.easyid3 import EasyID3
import MySQLdb as mariadb
import os
import re
import sys

class musicfile():

    def __init__(self):
        self.album_artist = ""
        self.album = ""
        self.year = ""
        self.disc = ""
        self.track = ""
        self.title = ""
        self.length_hr = 0
        self.length_min = 0
        self.length_sec = 0
        self.length = "{:02d}{:02d}{:02d}".format(self.length_hr, self.length_min, self.length_sec)
        self.artistid = 0
        self.albumid = 0
        self.format = ""

    def set_from_vorbistags(self, f):
        t = f.tags
        self.album_artist = t["ALBUMARTIST"][0]
        self.album = t["Album"][0]
        self.year = str(t["Date"][0])
        self.disc = str(t["DISCNUMBER"][0])
        self.track = str(t["tracknumber"][0])
        self.title = t["title"][0]
        self.length_hr = int(f.info.length / 3600)
        self.length_min = int(f.info.length - (self.length_hr * 3600) / 60)
        self.length_sec = int(f.info.length) % 60
        self.length = "{:02d}{:02d}{:02d}".format(self.length_hr, self.length_min, self.length_sec)

    def set_from_id3(self, f):
        t = f.tags
        self.album_artist = t["ALBUMARTIST"][0]
        self.album = t["Album"][0]
        self.year = str(t["Date"][0])
        self.disc = str(self.retrieve_numerics(t["DISCNUMBER"][0]))
        self.track = str(self.retrieve_numerics(t["tracknumber"][0]))
        self.title = t["title"][0]
        self.length_hr = int(f.info.length / 3600)
        self.length_min = int((f.info.length - (self.length_hr * 3600)) / 60)
        self.length_sec = int(f.info.length) % 60
        self.length = "{:02d}{:02d}{:02d}".format(self.length_hr, self.length_min, self.length_sec)

    def retrieve_numerics(self, src):
        numerics = re.findall("\d+", src)
        return int(numerics[0])

    def setArtistID(self, conn):
        cursor = conn.cursor()
        sql = "SELECT artistid FROM artist WHERE artistname='{}';".format(self.make_safe(self.album_artist))
        result = cursor.execute(sql)
        if  result != 0:
            row = cursor.fetchone()
            self.artistid = row[0]


    def setAlbumID(self, conn):
        cursor = conn.cursor()
        sql = "SELECT albumid FROM album WHERE album='{}' AND artistid={};".format(self.make_safe(self.album),
                                                                                   self.artistid)
        result = cursor.execute(sql)
        if result != 0:
            row=cursor.fetchone()
            self.albumid = row[0]


    def setTrackID(self, conn):
        cursor = conn.cursor()
        sql = "SELECT trackid FROM track WHERE albumid={} " \
              "AND disc={} and track={};".format(self.albumid, self.disc, self.track)
        result = cursor.execute(sql)
        if result == 0:
            return 0
        else:
            return cursor.fetchone()[0]

    def make_safe(self, s):
        return s.replace("'", "''")

    def insertTrack(self, conn, file, format):
        cursor = conn.cursor()
        trackid = self.setTrackID(conn)

        if trackid != 0:
            cursor.execute("UPDATE track SET {}_loc = '{}' WHERE TrackID={};".format(format,
                                                                                     self.make_safe(file), trackid))

        conn.commit()

def main():
    conn = mariadb.connect(user='simon', passwd='phaedra74', db='catalogue', use_unicode=True, charset='utf8')

    error_files = []

    for format in ['flac', 'mp3']:

        basedir = "/mnt/audio/" + format.upper()

        for root, dirs, files in os.walk(basedir):
            for f in files:
                if f.endswith("." + format):
                    print("Scanning : " + f)
                    file = os.path.join(root, f)
                    m = musicfile()
                    if format == 'flac':
                        f = flac.FLAC(file)
                        m.set_from_vorbistags(f)
                    else:
                        f = mp3.MP3(file, ID3=EasyID3)
                        m.set_from_id3(f)

                    m.setArtistID(conn)
                    m.setAlbumID(conn)
                    m.insertTrack(conn, file, format)

if __name__ == '__main__':
    main()