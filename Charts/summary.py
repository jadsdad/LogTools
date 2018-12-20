import MySQLdb as mariadb
from pathlib import Path
import os
import io

basedir = str(Path.home()) + "/Charts"
conn = mariadb.connect(user='root', passwd='3amatBotMfO', db='catalogue', use_unicode=True, charset='utf8')
seperator = "-" * 60 + "\n"

def update_data():
    cursor = conn.cursor()
    cursor.execute("CREATE TEMPORARY TABLE peak_albums_table SELECT * FROM peaks_album;")
    conn.commit()

def query_db(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_artists():
    sql = "SELECT DISTINCT artistname FROM peak_albums_table ORDER BY artistname;"
    return query_db(sql)

def get_albums(artistname):
    artistname_safe = artistname.replace("'","''")
    sql = "SELECT DISTINCT y, album FROM peak_albums_table " \
          "WHERE artistname='{}' ORDER BY y, album;".format(artistname_safe)
    return query_db(sql)

def get_peak(artistname, album, ranktype):
    artistname_safe = artistname.replace("'", "''")
    album_safe = album.replace("'","''")
    sql = "SELECT peak FROM peak_albums_table " \
          "WHERE artistname='{}' and album='{}'".format(artistname_safe, album_safe, ranktype)
    row = query_db(sql)
    if len(row) == 0:
        return None
    else:
        return row[0][0]


def generate_summary():
    update_data()
    f = open(os.path.join(basedir, "Album Peak Summary.txt"), "w")
    artists = get_artists()
    for art in artists:
        art_name = art[0]
        print(art_name)
        f.write(seperator)
        f.write("{:<55}{:>5}\n".format(art_name.upper(), "ALB"))
        f.write(seperator + "\n")

        albums = get_albums(art_name)

        for alb in albums:
            y = alb[0]
            alb_title = alb[1]
            print("--" + alb_title)
            linestring = ""
            alb_peak = get_peak(art_name, alb_title, "Album")
            alb_title = alb_title[:40]
            linestring = "{:<10}{:<45}{:>5}\n".format(y, alb_title,
                                                           "--" if alb_peak is None else alb_peak)
            f.write(linestring)
        f.write("\n\n")

    f.flush()
    f.close()
    conn.close()

if __name__ == '__main__':
    generate_summary()

