import pandas as pd
import matplotlib.pyplot as plt
import logtools_common as common

conn = common.conn

plt.rcParams['figure.figsize'] = (15,5)

df = pd.read_sql("SELECT logdate, count(logid) as plays from log group by logdate order by logdate;", conn, index_col=['logdate'], parse_dates=['logdate'])

df.loc[:,'weekday'] = df.index.weekday

weekday_counts = df.groupby('weekday').aggregate(sum)
weekday_counts.index = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
ax = weekday_counts.plot(kind='bar')
fig = ax.get_figure()
fig.savefig('test.pdf')