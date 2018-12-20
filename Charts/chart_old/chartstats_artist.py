import MySQLdb as mariadb
from pathlib import Path
import io

basedir = str(Path.home()) + "/Charts"
ranktypes = ['Artist - Month', 'Artist - Year']
conn = mariadb.connect(user='root', passwd='3amatBotMfO', db='catalogue', use_unicode=True, charset='utf8')

def get_rows_from_sql(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_artists():
    sql = "SELECT DISTINCT artistname FROM chartstats_view order by artistname;"
    return get_rows_from_sql(sql)

def get_art_history(artname, ranktype):
    artname_safe = artname.replace("'", "''")
    sql = "SELECT y, m, rank FROM chartstats_view " \
          "where artistname='{}' and ranktype='{}' order by y, m;".format(artname_safe, ranktype)
    return get_rows_from_sql(sql)

def get_max_rank(y, m, ranktype):
    sql = "SELECT MAX(rank) as maxrank from chartstats_view " \
          "where y={} and m={} and ranktype='{}';".format(y, m, ranktype)
    return get_rows_from_sql(sql)[0][0]

def generate_report():
    f = io.open(basedir + "/Chart Stats - Artist.txt","w",encoding='utf-8')
    marray = ['', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    art_list = get_artists()
    for art in art_list:
        art_name = art[0]
        f.write("{0}\n{1}\n{0}\n\n".format("=" * 80, art_name.upper()))
        for rt in ranktypes:
            f.write("\t" + rt + "\n\n")
            art_history = get_art_history(art_name, rt)
            for h in art_history:
                y = h[0]
                m = h[1]
                r = h[2]
                maxrank = get_max_rank(y, m, rt)
                f.write("\t\t{} {:<20}{:>3} / {:>3}\n".format(y, marray[m], r, maxrank))
            f.write("\n\n")
    f.flush()
    f.close()

if __name__ == '__main__':
    generate_report()