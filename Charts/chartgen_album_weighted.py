import MySQLdb as mariadb
from pathlib import Path
import os
import io
import shutil
import filecmp
from datetime import date, timedelta
from decimal import *

basedir = str(Path.home()) + "/Charts"
conn = mariadb.connect(user='root', passwd='3amatBotMfO', db='catalogue', use_unicode=True, charset='utf8')
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

    if len(data) > 0:
        f = io.open(os.path.join(basedir, outfile), "w", encoding='utf-8')
        f.write(seperator)
        datadict = []
        rank = 1
        for dataline in data:
            textline = ""
            art = dataline[0][:40]
            album = dataline[1]
            logtime = int(dataline[2])
            logcount = int(dataline[3])
            weighted_score = (((logtime / totaltime) * 0.5) +((logcount / totalplays) * 0.5)) * 100000
            datadict_line = [art, album, weighted_score]
            datadict.append(datadict_line)
        s = sorted(datadict, key=lambda x: x[2], reverse=True)

        for row in s:
            art, album, score = row[:3]
            textline = "{:<5}{:<80}{:>10.2f}\n{:<5}{:<80}\n".format(rank, art.upper(), score, '', album)
            f.write(textline)
            f.write(seperator)
            rank += 1

        f.flush()
        f.close()

def run():

    generate_chart("Album Chart (Weighted).txt", get_data("chart_album_alltime"), basedir)
    for y in range(2018, date.today().year + 1):
        generate_chart("Album Chart (Weighted) - {}.txt".format(y), get_data("charts_yearly", "YearReleased={}".format(y)), basedir + "/Yearly")

if __name__ == '__main__':
    run()