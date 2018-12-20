from random import randrange
import MySQLdb as mariadb
from datetime import timedelta, datetime

conn = mariadb.connect(user='root', passwd='3amatBotMfO', db='catalogue', use_unicode=True, charset='utf8')

def random_date(start, end):
    delta = end - start
    int_delta = delta.days
    random_day = randrange(int_delta)
    return start + timedelta(days=random_day)

def get_albumcount():
    sql = "Select * from album;"
    rows = conn.cursor().execute(sql)
    return rows

def main():
    upperidbound = get_albumcount()
    mindate = datetime.strptime("01-01-2017", "%d-%m-%Y")
    maxdate = datetime.strptime("31-12-2019", "%d-%m-%Y")

    curdate = mindate
    delta = timedelta(days=1.0)

    while curdate <= maxdate:
        curdatestr = curdate.strftime("%Y-%m-%d")
        print(curdatestr)
        for f in range(1, randrange(2, 5)):
            albumid = randrange(upperidbound)
            sql = "INSERT INTO log (AlbumID, LogDate) VALUES ({}, '{}');".format(albumid, curdatestr)
            try:
                x = conn.cursor().execute(sql)
                conn.commit()
            except mariadb.IntegrityError:
                pass
        curdate = curdate + timedelta(days=1)

if __name__ == '__main__':
    main()
