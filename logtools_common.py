import MySQLdb as mariadb
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

conn = mariadb.connect(db='catalogue', use_unicode=True, charset='utf8', read_default_file='~/.my.cnf')
basedir = str(Path.home()) + "/Charts"

def get_results(sql):
    c = conn.cursor()
    c.execute(sql)
    results = c.fetchall()
    return results


def execute_sql(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def format_to_MS(seconds):
    if type(seconds) == Decimal:
        seconds = float(seconds)

    mytime = timedelta(seconds=seconds)
    return "{:2d}:{:02d}".format(int(mytime.seconds // 60), int(mytime.seconds % 60))


def shorten_by_word(text, length):
    if text is None:
        return None

    wordsplit = text.split(" ")
    output = ""
    for w in wordsplit:
        if len(output) + len(w) < length:
            if len(output) > 0:
                output += " "
            output += w
        else:
            return output
    return output