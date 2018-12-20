import MySQLdb as mariadb
from pathlib import Path
import io

basedir = str(Path.home()) + "/Charts"
ranktypes = ['Album - Month', 'Album - Year',
             "Album - This Year's Purchases",
             "Album - This Year's Releases",
             "EP - Year"]

conn = mariadb.connect(user='root', passwd='3amatBotMfO', db='catalogue', use_unicode=True, charset='utf8')

def get_rows_from_sql(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_albums():
    sql = "SELECT DISTINCT artistname, album " \
          "FROM chartstats_view " \
          "WHERE album is not null order by artistname, album;"
    return get_rows_from_sql(sql)

def get_art_history(artname, album, ranktype):
    artname_safe = artname.replace("'", "''")
    album_safe = album.replace("'", "''")
    ranktype_safe = ranktype.replace("'", "''")

    sql = "SELECT y, m, rank FROM chartstats_view " \
          "where artistname='{}' and album='{}' and ranktype='{}' order by y, m;".format(artname_safe,
                                                                                         album_safe, ranktype_safe)
    return get_rows_from_sql(sql)

def get_max_rank(y, m, ranktype):
    ranktype_safe = ranktype.replace("'", "''")
    sql = "SELECT MAX(rank) as maxrank from chartstats_view " \
          "where y={} and m={} and ranktype='{}';".format(y, m, ranktype_safe)
    return get_rows_from_sql(sql)[0][0]

def generate_report():
    f = io.open(basedir + "/Chart Stats - Album.txt","w",encoding='utf-8')
    marray = ['', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    alb_list = get_albums()
    for art in alb_list:
        art_name = art[0]
        alb_name = art[1]
        f.write("{2}\n{0}\n{1}\n{2}\n\n".format(art_name.upper(), alb_name, "=" * 80))
        for rt in ranktypes:
            art_history = get_art_history(art_name, alb_name, rt)

            if len(art_history) > 0:
                f.write("\t" + rt + "\n\n")

                for h in art_history:
                    y = h[0]
                    m = h[1]
                    r = h[2]
                    maxrank = get_max_rank(y, m, rt)
                    f.write("\t\t{} {:<20}{:>3} / {:>3}\n".format(y, marray[m], r, maxrank))
                f.write("\n\n")
        f.write("\n\n")
    f.flush()
    f.close()

if __name__ == '__main__':
    generate_report()