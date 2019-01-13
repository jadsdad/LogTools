#!/usr/bin/python3

import MySQLdb as MariaDB
from datetime import timedelta
from pathlib import Path
import io

conn = MariaDB.connect(db='catalogue', use_unicode=True, charset='utf8', read_default_file='~/.my.cnf')


def analyse_tracks(albumid):
    trackcount = 0
    bonuscount = 0
    maintime = timedelta(seconds=0)
    bonustime = timedelta(seconds=0)

    sql = "SELECT * FROM track WHERE albumid={};".format(albumid)
    cursor = conn.cursor()
    cursor.execute(sql)
    tracklist = cursor.fetchall()
    for t in tracklist:
        trackcount += 1
        if t[6] == 1:
            bonuscount += 1
            bonustime += t[5]
        else:
            maintime += t[5]

    return trackcount, bonuscount, maintime, bonustime


def get_albumlist():
    sql = "SELECT artist.artistname, album.albumid, yearreleased, album FROM album " \
          "INNER JOIN albumartist on album.albumid = albumartist.albumid " \
          "INNER JOIN artist on albumartist.artistid = artist.artistid where sourceid <> 6 " \
          "order by artistname, yearreleased, album;"
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def main():
    albums = get_albumlist()
    f = io.open(str(Path.home()) + "\\Track Analysis.txt","w", encoding="utf-8")
    line = "{:<50}{:<80}{:<15}{:<15}{:<15}{:<15}{:<15}\n".format("ARTIST", "ALBUM", "YEAR", "TRKS", "BONUS", "TIME", "BONUS TIME")
    f.write(line)
    lastart = ""
    for a in albums:
        artist = a[0]
        albumid = a[1]
        year = a[2]
        albumtitle = a[3]
        t, b, mt, bt = analyse_tracks(albumid)
        if artist != lastart:
             f.write("\n")
        lastart = artist
        line = "{:<50}{:<80}{:<15}{:<15}{:<15}{:<15}{:<15}\n".format(artist[:40], albumtitle[:70], year, t, b, str(mt), str(bt))
        f.write(line)

    f.flush()
    f.close()

if __name__ == '__main__':
    main()
