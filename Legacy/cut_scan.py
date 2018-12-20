from mutagen import flac
import MySQLdb as mariadb
import os
import sys


def getArtistID(album_artist, conn):
    album_artist = album_artist.replace("'", "''")
    cursor = conn.cursor()
    sql = "SELECT artistid FROM artist WHERE artistname='{}';".format(album_artist)
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is None:
        return 0
    else:
        return row[0]


def getAlbumID(artistid, album, conn):
    album = album.replace("'", "''")
    cursor = conn.cursor()
    sql = "SELECT albumid FROM album WHERE album='{}' AND artistid={};".format(album, artistid)
    cursor.execute(sql)
    row = cursor.fetchone()
    return 0 if row is None else row[0]


def clearDB(conn):
    pass


def insertTrack(albumid, conn):
    if albumid is not None:
        cursor = conn.cursor()
        cursor.execute("UPDATE album SET MadeTheCut = 1 WHERE albumid = {}".format(albumid))
        conn.commit()
    else:
        print("AlbumID is None")


conn = mariadb.connect(user='simon', passwd='phaedra74', db='catalogue', use_unicode=True, charset='utf8')

error_files = []
basedir = "/home/simon/Archive-Keep/"

for root, dirs, files in os.walk(basedir):
    for f in files:
        if f.endswith(".flac"):
            print("Scanning : " + f)
            file = os.path.join(root, f)
            f = flac.FLAC(file)
            t = f.tags
            album_artist = t["ALBUMARTIST"][0]
            album = t["Album"][0]

            artistID = getArtistID(album_artist, conn)
            albumID = getAlbumID(artistID, album, conn)
            insertTrack(albumID, conn)
