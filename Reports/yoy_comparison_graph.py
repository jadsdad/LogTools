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

def get_weekstats(y):
    sql = "SELECT * FROM listen_perweek where Y = {} and w between 2 and 52 order by w;".format(y)
    results = query_db(sql)
    return results

outfile = str(Path.home()) + "/Charts/YOY Comparison.pdf"

weekrange=range(2, 53)

for y in range(2018, date.today().year + 1):
    dataplot = []
    weekplot = []
    data = get_weekstats(y)
    for d in data:
        w = d[1]
        t = d[2]
        weekplot.append(w)
        dataplot.append(t)
    plt.plot(weekplot, dataplot, label=y)
    plt.legend()

plt.title("Year-on-Year Comparison")
plt.xlabel("Calendar Week")
plt.ylabel("Time (hours)")
plt.grid(True)
plt.axis(xmin=1, xmax=53)
plt.axvline(x=11, color='red', linestyle='--', lw=0.5)
plt.savefig(outfile, format="pdf")
