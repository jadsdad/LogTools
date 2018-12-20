#!/usr/bin/python3

from mutagen import flac
import MySQLdb as mariadb
import os, sys, traceback

basedir = "/home/simon/Archive/"
conn = mariadb.connect(user='simon', passwd='phaedra74', db='catalogue', use_unicode=True, charset='utf8')

def reset():
    cursor = conn.cursor()
    cursor.execute("UPDATE album SET audit = NULL;")
    conn.commit()
    cursor.execute("UPDATE track SET audit = NULL;")
    conn.commit()

def doScan():
    reset()
    for root, dirs, files in os.walk(basedir):
        for f in files:
            if f.endswith(".flac"):
                file = os.path.join(root, f)
                try:
                    f = flac.FLAC(file)
                    t = f.tags
                    album_artist = t["ALBUMARTIST"][0]
                    album = t["Album"][0]
                    year = str(t["Date"][0])
                    trackartist = str(t["artist"][0])
                    disc = str(t["DISCNUMBER"][0])
                    track = str(t["tracknumber"][0])
                    title = t["title"][0]
                    length_hr = int((f.info.length) / 3600)
                    length_min = int((f.info.length - (length_hr * 3600)) / 60)
                    length_sec = int(f.info.length) % 60
                    length = "{:02d}{:02d}{:02d}".format(length_hr, length_min, length_sec)

                    print("Scanned >> {}: {}".format(album_artist, title))

                    artistID = getArtistID(album_artist)
                    albumID = getAlbumID(artistID, album, year)
                    insertTrack(albumID, disc, track, title, length, trackartist)

                except:
                    print("--- ERROR IN FILE HEADER: " + traceback.format_exc())

    #os.system("mv -v /home/simon/Rips/Scan/* /home/simon/Rips/Archive/")
    # os.system("mkdir '/home/simon/Rips/Scan to DB/'")


def getArtistID(album_artist):
    cursor = conn.cursor()
    sql = "SELECT artistid FROM artist WHERE artistname=%s;"
    result = cursor.execute(sql, (album_artist,))
    if result == 0:
        cursor.execute("INSERT INTO artist (artistname) VALUES (%s);", (album_artist,))
        conn.commit()
        return cursor.lastrowid
    else:
        row = cursor.fetchone()
    return row[0]


def getAlbumID(artistid, album, year):
    cursor = conn.cursor()
    sql = "SELECT albumid FROM album WHERE album=%s AND artistid=%s;"
    result = cursor.execute(sql, (album, artistid,))
    if result == 0:
        cursor.execute("INSERT INTO album (album, yearreleased, artistid, albumtypeid, audit) VALUES (%s,%s,%s,12, 1);",
                       (album, year, artistid,))
        conn.commit()
        return cursor.lastrowid
    else:
        row = cursor.fetchone()
        auditAlbum(row[0])
        return row[0]


def getTrackID(albumid, disc, track):
    cursor = conn.cursor()
    sql = "SELECT trackid FROM track WHERE albumid=%s AND disc=%s and track=%s;"
    result = cursor.execute(sql, (albumid, disc, track,))
    if result == 0:
        return 0
    else:
        return cursor.fetchone()[0]


def auditAlbum(albumid):
    cursor = conn.cursor()
    cursor.execute("UPDATE album SET audit = 1 WHERE albumid = %s", (albumid,))
    conn.commit()


def insertTrack(albumid, disc, track, title, length, trackartist):
    cursor = conn.cursor()
    trackid = getTrackID(albumid, disc, track)

    if trackid == 0:
        cursor.execute("INSERT INTO track (albumid, disc, track, tracktitle, "
                       "length, audit) VALUES (%s,%s,%s,%s,%s,1);", (albumid, disc, track, title, length,))
    else:
        cursor.execute("UPDATE track SET tracktitle = %s, length = %s, audit = 1 "
                       "WHERE trackid = %s", (title, length, trackid,))

    conn.commit()


if __name__ == "__main__":
    doScan()
