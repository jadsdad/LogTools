import MySQLdb as mariadb
from pathlib import Path
import os
import io
import shutil
import filecmp
from datetime import date, timedelta

basedir = str(Path.home()) + "/Charts"
conn = mariadb.connect(db='catalogue', use_unicode=True, charset='utf8')
seperator = "-" * 100 + "\n"

def query_db(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_data(query, condition=None):
    sql = "SELECT ArtistName, Album, Points, Plays from {} ".format(query)

    if condition is not None:
        sql += "WHERE {} ".format(condition)

    sql += "LIMIT 100;".format(query.lower())

    return query_db(sql)

def generate_chart(outfile, data, basedir):
    if len(data) > 0:
        f = io.open(os.path.join(basedir, outfile), "w", encoding='utf-8')
        f.write(seperator)

        rank = 1
        for dataline in data:
            textline = ""
            art = dataline[0][:40]
            alb = dataline[1][:40]
            logtime = dataline[2]
            logcount = dataline[3]

            if alb is None:
                textline = "{:<5}{:<80}{:>10}\n".format(rank, art.upper(), logtime)
            else:
                textline = "{:<5}{:<80}{:>10} pts\n{:<5}{:<80}{:>10} pls\n".format(rank, art.upper(), logtime, '', alb, logcount)

            f.write(textline)
            f.write(seperator)
            rank += 1

        f.flush()
        f.close()

def run():

    generate_chart("Artist Chart.txt", get_data("chart_artist_alltime"), basedir)
    generate_chart("Album Chart.txt", get_data("chart_album_alltime"), basedir)
    for y in range(2018, date.today().year + 1):
        generate_chart("Album Chart - {}.txt".format(y), get_data("charts_yearly", "YearReleased={}".format(y)), basedir + "/Yearly")

if __name__ == '__main__':
    run()