import matplotlib.pyplot as plt
import MySQLdb as mariadb

conn = mariadb.connect(user='root', passwd='3amatBotMfO', db='catalogue', use_unicode=True, charset='utf8')

def get_data(yr):
    sql = "select * from listen_by_week where Y={}".format(yr)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    xaxis = []
    yaxis = []
    for row in data:
        xaxis.append(row[1])
        yaxis.append(row[2])

    return xaxis, yaxis



def run():
    xaxis, yaxis = get_data(2018)
    plt.plot(xaxis, yaxis)
    f = open("/home/simon/test.png", "wb")
    plt.savefig(f, dpi=300, format="png")
    f.close()

if __name__ == '__main__':
    run()
