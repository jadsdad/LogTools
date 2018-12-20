from mutagen import oggvorbis
import MySQLdb as mariadb
import os
import sys

def getArtistID(album_artist, conn):
    cursor = conn.cursor()
    sql = "SELECT ArtistID FROM Artist WHERE ArtistName=%s;"
    result = cursor.execute(sql,(album_artist, ))
    if  result == 0:
        cursor.execute("INSERT INTO Artist (ArtistName) VALUES (%s);",(album_artist, ))
        conn.commit()
        return cursor.lastrowid
    else:
        row = cursor.fetchone()
        return row[0]


def getAlbumID(artistid, album, year, conn):
    cursor = conn.cursor()
    sql = "SELECT AlbumID FROM Album WHERE Album=%s AND ArtistID=%s;"
    result = cursor.execute(sql, (album, artistid, ))
    if result == 0:
        cursor.execute("INSERT INTO Album (Album, YearReleased, ArtistID) VALUES (%s,%s,%s);", (album, year, artistID, ))
        conn.commit()
        return cursor.lastrowid
    else:
        row=cursor.fetchone()
        return row[0]

def clearDB(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE from Artist;")
    conn.commit()


def getTrackID(albumid, disc, track, conn):
    cursor = conn.cursor()
    sql = "SELECT trackid FROM track WHERE albumid=%s AND disc=%s and track=%s;"
    result = cursor.execute(sql, (albumid, disc, track,))
    if result == 0:
        return 0
    else:
        return cursor.fetchone()[0]


def insertTrack(albumid, disc, track, title, length, conn):
    cursor = conn.cursor()
    trackid = getTrackID(albumid, disc, track, conn)

    if trackid == 0:
        cursor.execute("INSERT INTO track (albumid, disc, track, tracktitle, "
                       "length) VALUES (%s,%s,%s,%s,%s);", (albumid, disc, track, title, length, ))
    else:
        cursor.execute("UPDATE track SET tracktitle = %s, length = %s, "
                       "WHERE trackid = %s", (title, length, trackid, ))

    conn.commit()


conn = mariadb.connect(user='root', passwd='3amatBotMfO', db='Catalogue', use_unicode=True, charset='utf8')

error_files = []
basedir = "c:/Builds in Progress/Test"

clearDB(conn)

for root, dirs, files in os.walk(basedir):
    for f in files:
        if f.endswith(".ogg"):
            print("Scanning : " + f)
            file = os.path.join(root, f)
            try:
                f = oggvorbis.OggVorbis(file)
                t = f.tags
                album_artist = t["ALBUMARTIST"][0]
                album = t["Album"][0]
                year = str(t["Date"][0])
                disc = str(t["DISCNUMBER"][0])
                track = str(t["tracknumber"][0])
                title = t["title"][0]
                length_hr = int((f.info.length) / 3600)
                length_min = int((f.info.length - (length_hr*3600)) / 60)
                length_sec = int(f.info.length) % 60
                length = "{:02d}{:02d}{:02d}".format(length_hr, length_min, length_sec)

                artistID = getArtistID(album_artist, conn)
                albumID = getAlbumID(artistID, album, year, conn)
                insertTrack(albumID, disc, track, title, length, conn)

            except oggvorbis.OggVorbisHeaderError:
                print("--- ERROR IN FILE HEADER")
                error_files.append(file)

ef = open("errorfiles.txt","a")
for x in error_files:
    ef.write(x + "\n")
ef.flush()
ef.close()