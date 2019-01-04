import matplotlib.pyplot as plt
import MySQLdb as mariadb
import io
from pathlib import Path

from datetime import date

conn = mariadb.connect(user='root', passwd='3amatBotMfO', db='catalogue', use_unicode=True, charset='utf8')

def query_db(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_mediastats(media):
    sql = "SELECT DATE_FORMAT(log.logdate, '%b %Y') as M, " \
          "source.Source as Source, count(log.logID) as Plays " \
          "FROM log INNER JOIN album ON log.AlbumID = album.AlbumID " \
          "inner join source on album.SourceID = source.sourceid " \
          "WHERE source = '{}' " \
          "GROUP BY M, Source ORDER BY logdate, Source;".format(media)
    results = query_db(sql)
    return results

outfile = str(Path.home()) + "/Charts/Media Comparison.pdf"

total = []
index=1
for media in ['Vinyl','CD','Digital','Cassette','Streamed']:
    dataplot = []
    monthplot = []
    data = get_mediastats(media)
    t = 0
    for d in data:
        m = d[0]
        t += d[2]
        monthplot.append(m)
        dataplot.append(t)
    plt.plot(monthplot, dataplot, label=media)

plt.legend(fontsize='x-small')
plt.grid(axis='x', color='lightgrey', linestyle='--', markevery=3)
plt.grid(axis='y', color='lightgrey', linestyle='--')
plt.tick_params(axis='both', labelsize=6)
plt.xticks(rotation=90)

plt.savefig(outfile, dpi=2400, format="pdf")
