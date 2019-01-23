import matplotlib.pyplot as plt
import MySQLdb as mariadb
import io
from pathlib import Path
from datetime import date

conn = mariadb.connect(db='catalogue', use_unicode=True, charset='utf8', read_default_file='~/.my.cnf')

def query_db(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_mediastats(media, y):
    sql = "SELECT YEAR(log.logdate) as Y, " \
          "MONTH(log.logdate) as M, " \
          "source.Source as Source, count(log.logID) as Plays " \
          "FROM log INNER JOIN album ON log.AlbumID = album.AlbumID " \
          "inner join source on album.SourceID = source.sourceid " \
          "WHERE source = '{}' and year(log.logdate)={} " \
          "GROUP BY Y, M, Source ORDER BY logdate, Source;".format(media, y)
    results = query_db(sql)
    return results

def run():
    total = []
    index=1
    for y in range(2018, date.today().year + 1):
        outfile = str(Path.home()) + "/Charts/Yearly/Media Comparison - {}.pdf".format(y)
        for media in ['Vinyl','CD','Digital','Cassette']:
            dataplot = []
            monthplot = []
            data = get_mediastats(media, y)
            t = 0
            for d in data:
                m = d[1]
                t = d[3]
                monthplot.append(m)
                dataplot.append(t)
            plt.plot(monthplot, dataplot, label=media)

        plt.legend(fontsize='x-small')
        plt.grid(axis='x', color='lightgrey', linestyle='--', markevery=3)
        plt.grid(axis='y', color='lightgrey', linestyle='--')
        plt.tick_params(axis='both', labelsize=6)
        plt.xticks(rotation=90)
        plt.axis(xmin=1, xmax=12)
        plt.savefig(outfile, dpi=2400, format="pdf")
        plt.close()

if __name__ == '__main__':
    run()