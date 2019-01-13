import MySQLdb as mariadb
from pathlib import Path
import os
import io
import shutil
import filecmp
from datetime import date, timedelta
from decimal import *

basedir = str(Path.home()) + "/Charts"
conn = mariadb.connect(db='catalogue', use_unicode=True, charset='utf8', read_default_file='~/.my.cnf')
seperator = "-" * 100 + "\n"
totalplays = 0
totaltime = 0


def query_db(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_total_plays():
    sql = "SELECT SUM(playcount) FROM album where SourceID<>6;"
    results = get_results(sql)
    return results[0][0]

def get_total_albums():
    sql = "SELECT COUNT(*) FROM album where SourceID<>6;"
    results = get_results(sql)
    return results[0][0]

def get_albums_by_artist(artistname):
    sql = "SELECT COUNT(album.albumid) " \
          "FROM album " \
          "INNER JOIN albumartist ON album.albumid = albumartist.albumid " \
          "INNER JOIN artist on albumartist.artistid = artist.artistid " \
          "WHERE SourceID<>6 and artist.artistname='{}';".format(artistname.replace("'","''"))
    results = get_results(sql)
    return results[0][0]

def get_played_by_artist(artistname):
    sql = "SELECT SUM(album.played) " \
          "FROM album " \
          "INNER JOIN albumartist ON album.albumid = albumartist.albumid " \
          "INNER JOIN artist on albumartist.artistid = artist.artistid " \
          "WHERE SourceID<>6 and artist.artistname='{}';".format(artistname.replace("'","''"))
    results = get_results(sql)
    return results[0][0]

def get_total_time():
    sql = "SELECT SUM(tracklength) FROM tracklengths where bonustrack = 0;"
    results = get_results(sql)
    return results[0][0]

def get_results(sql):
    c = conn.cursor()
    c.execute(sql)
    results = c.fetchall()
    return results

def get_data(query, condition=None):
    sql = "SELECT ArtistName, Album, Points, Plays from {} ".format(query)

    if condition is not None:
        sql += "WHERE {} ".format(condition)

    sql += "LIMIT 100;".format(query.lower())

    return query_db(sql)

def generate_chart(outfile, data, basedir):
    totalplays = int(get_total_plays())
    totaltime = int(get_total_time())
    totalalbums = int(get_total_albums())

    if len(data) > 0:
        f = io.open(os.path.join(basedir, outfile), "w", encoding='utf-8')
        f.write(seperator)
        datadict = {}
        rank = 1
        for dataline in data:
            textline = ""
            art = dataline[0][:40]
            logtime = int(dataline[2])
            logcount = int(dataline[3])
            albcount = int(get_albums_by_artist(art))
            artplayed = int(get_played_by_artist(art))
            weighted_score = (((logtime / totaltime) * 0.5) + \
                             ((logcount / totalplays) * 0.5)) * 100000

            datadict[art] = weighted_score

        s = [(k, datadict[k]) for k in sorted(datadict, key=datadict.get, reverse=True)]

        for key, value in s:
            textline = "{:<5}{:<80}{:>10.2f}\n".format(rank, key, datadict[key])

            f.write(textline)
            f.write(seperator)
            rank += 1

        f.flush()
        f.close()

def run():

    generate_chart("Artist Chart (Weighted).txt", get_data("chart_artist_alltime"), basedir)

if __name__ == '__main__':
    run()