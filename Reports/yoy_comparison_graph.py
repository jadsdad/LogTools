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

def get_weekstats(y):
    sql = "SELECT * FROM listen_permonth where Y = {} order by m;".format(y)
    results = query_db(sql)
    return results

outfile = str(Path.home()) + "/Charts/YOY Comparison.pdf"

monthrange=range(1, 12)
total = []

for y in range(2018, date.today().year + 1):
    dataplot = []
    weekplot = []
    data = get_weekstats(y)
    for d in data:
        w = d[1]
        t = d[2]
        weekplot.append(w)
        dataplot.append(t)
        total.append(t)
    plt.plot(weekplot, dataplot, label=y)


monthly_average = sum(total) / len(total)

plt.title("Year-on-Year Comparison")
plt.xlabel("Calendar Week")
plt.ylabel("Time (hours)")
plt.grid(axis='x', color='lightgrey', linestyle='--', markevery=3)
plt.grid(axis='y', color='lightgrey', linestyle='--')
plt.axis(xmin=1, xmax=12)
plt.axhline(y=monthly_average, color='red', linestyle='--', lw=0.5)
plt.legend(fontsize='x-small')
plt.savefig(outfile, dpi=1200, format="pdf")
