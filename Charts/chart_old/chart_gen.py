#!/usr/bin/python3

import MySQLdb as mariadb
from pathlib import Path
import io
import chartstats_artist
import chartstats_album

basedir = str(Path.home()) + "/Charts"

conn = mariadb.connect(user='root', passwd='3amatBotMfO', db='catalogue', use_unicode=True, charset='utf8')

def get_rows_from_sql(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def execute_sql(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def get_chart_list():
    sql = "SELECT * FROM ranktype;"
    return get_rows_from_sql(sql)


def get_chart_data(rankid, y, m):
    sql = "SELECT * FROM chartstats WHERE ranktypeid = {} AND y={} AND m={}".format(rankid, y, m)
    return get_rows_from_sql(sql)


def get_periods(rankid):
    sql = "SELECT DISTINCT y, m FROM chartstats WHERE ranktypeid = {}".format(rankid)
    return get_rows_from_sql(sql)


def get_artname(artistid):
    sql = "SELECT artistname FROM artist WHERE artistid = {}".format(artistid)
    return get_rows_from_sql(sql)[0][0]


def get_albumtitle(albumid):
    sql = "SELECT album FROM album WHERE albumid = {}".format(albumid)
    return get_rows_from_sql(sql)[0][0]

def generate_filename(ranktype, y, m):
    filename = "{}/{} {} {}".format(basedir, ranktype,
                                 '' if y == 0 else y,
                                 '' if m == 0 else str(m).zfill(2)).rstrip()
    filename = filename + ".txt"
    return filename

def get_previous_rank(y, m, artname, album, ranktype, artistonly):
    m -= 1 if m > 0 else m
    if m <= 0:
        y -= 1

    if "Month" in ranktype and m == 0:
        m = 12

    artname_safe = artname.replace("'", "''")
    ranktype_safe = ranktype.replace("'", "''")

    if artistonly:
        sql = "SELECT rank FROM chartstats_view " \
              "where artistname='{}' and ranktype='{}' " \
              "and y = {} and m = {};".format(artname_safe, ranktype_safe, y, m)
    else:
        album_safe = album.replace("'", "''")
        sql = "SELECT rank FROM chartstats_view " \
              "where artistname='{}' and album='{}' and ranktype='{}' " \
              "and y = {} and m = {};".format(artname_safe, album_safe, ranktype_safe, y, m)

    output = get_rows_from_sql(sql)
    if len(output) == 0:
        return 0
    else:
        return output[0][0]

def main():
    execute_sql("CALL update_chartstats();")
    chartlist = get_chart_list()
    for chart in chartlist:
        rankid = chart[0]
        ranktype = chart[1]
        artistonly = True if "Artist" in ranktype else False
        periods = get_periods(rankid)
        for period in periods:
            y = period[0]
            m = period[1]
            f = io.open(generate_filename(ranktype, y, m), "w", encoding="utf-8")
            chartdata = get_chart_data(rankid, y, m)
            for ranking in chartdata:
                rank = ranking[2]
                points = "{:,} pts".format(ranking[5])
                plays = "{:,} pls".format(ranking[6])
                artistname = get_artname(ranking[3])[0:50]
                albumtitle = get_albumtitle(ranking[4])[0:50] if not artistonly else ""

                if "All Time" in ranktype:
                    lastrankstr = ""
                else:
                    lastrank = get_previous_rank(y, m, artistname, albumtitle, ranktype, artistonly)
                    lastrankstr = ""
                    if not lastrank == 0:
                        if rank > lastrank:
                            movestr = "-"
                        elif rank < lastrank:
                            movestr = "+"
                        else:
                            movestr = "="

                        lastrankstr = " ({}{})".format(movestr, lastrank)

                linestr = ""
                if artistonly:
                    linestr = "{:<15}{:<50}{:>15}\n{:>80}\n".format(str(rank) + lastrankstr, artistname.upper(),
                                                                          points, plays)
                else:
                    linestr = "{:<15}{:<50}{:>15}\n{:<15}{:<50}{:>15}\n".format(str(rank) + lastrankstr, artistname.upper(), points,
                                                                            '', albumtitle, plays)
                linestr += "-" * 80 + "\n"
                f.write(linestr)
                f.flush()
            f.close()

    chartstats_artist.generate_report()
    chartstats_album.generate_report()

if __name__ == '__main__':
    main()
