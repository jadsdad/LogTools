import MySQLdb as mariadb
from pathlib import Path
import os
import io
import shutil
import filecmp
from datetime import date, timedelta

basedir = str(Path.home()) + "/Charts"
conn = mariadb.connect(user='root', passwd='3amatBotMfO', db='catalogue', use_unicode=True, charset='utf8')
seperator = "-" * 100 + "\n"

def query_db(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def update_data():
    cursor = conn.cursor()

    cursor.execute("CREATE TEMPORARY TABLE rollingchart_table "
                   "SELECT 2 as RankType, `index`, `rank`, artistid, albumid, artistname, album, logtime, logcount "
                   "FROM chart_album_rolling "
                   "WHERE chart_album_rolling.rank <= 20;")

    cursor.execute("INSERT INTO rollingchart_table "
                    "SELECT 1 as ranktype, `index`, `rank`, artistid, 0 as albumid, "
                    "artistname, '' as album, logtime, logcount "
                    "FROM chart_artist_rolling "
                    "WHERE chart_artist_rolling.rank <= 30;")


    conn.commit()

def get_ranktypes():
    sql = "SELECT * from ranktype;"
    return query_db(sql)

def get_last_week():
    sql = "SELECT Max(`index`) as LastWeek from rollingchart_table;"
    return query_db(sql)[0][0]

def get_report_date(index):
    sql = "SELECT reportdate from rolling4weeks where `index`={};".format(index)
    row = query_db(sql)
    return row[0][0]

def get_threshold():
    d = date.today() - timedelta(days=7)
    return d

def get_data(query, condition=None):
    sql = "SELECT ArtistName, Album, Points, Plays from {} ".format(query)

    if condition is not None:
        sql += "WHERE {} ".format(condition)

    sql += "LIMIT 100;".format(query.lower())

    return query_db(sql)

def generate_chart(outfile, data):
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
            textline = "{:<5}{:<40}{:<40}{:>10}{:>5}\n".format(rank, art.upper(), alb, logtime, logcount)

        f.write(textline)
        f.write(seperator)
        rank += 1

    f.flush()
    f.close()

def run():
    generate_chart("Artist Chart.txt", get_data("chart_artist_alltime"))
    generate_chart("Album Chart.txt", get_data("chart_album_alltime"))
    for y in range(2018, date.today().year + 1):
        generate_chart("Album Chart - {}.txt".format(y), get_data("charts_yearly", "YearReleased={}".format(y)))

if __name__ == '__main__':
    run()