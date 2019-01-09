import MySQLdb as MariaDB
import io
import os
import sys
import os
from pathlib import Path

conn = MariaDB.connect(db='catalogue', use_unicode=True, charset='utf8')

f = None

albumcount = 0
logcount = 0
albumsplayed = 0
basedir = str(Path.home()) + "/Charts"


def openreportfile():
    global f
    f = io.open(os.path.join(basedir, "Stats.txt"), "w", encoding='utf-8')

def get_results(sql):
    c = conn.cursor()
    c.execute(sql)
    results = c.fetchall()
    return results

def shorten_by_word(text, length):
    wordsplit = text.split(" ")
    output = ""
    for w in wordsplit:
        if len(output) + len(w) < length:
            if len(output) > 0:
                output += " "
            output += w
    return output

# ALBUMS SECTION

def albums_by_format():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>11}{:>10}{:>11}{:>10}{:>11}{:>10}\n".format("by Format", "Count", "%", "Plays", "%", "Played", "%", "Ratio"))
    f.write("-" * 105 + "\n")
    sql = "SELECT source, COUNT(albumid) as SourceCount, SUM(playcount) as PlayCount, Sum(played) as Played FROM album inner join source on " \
          "album.sourceid = source.sourceid where album.sourceid<>6 GROUP BY source ORDER BY SourceCount desc;"
    results = get_results(sql)

    for r in results:
        source = r[0]
        count = int(r[1])
        percent = 0 if albumcount == 0 else (count/albumcount) * 100
        playcount = int(r[2])
        logpercent = 0 if logcount == 0 else (playcount/logcount) * 100
        played = int(r[3])
        playedpercent = 0 if count == 0 else (played / count) * 100
        ratio = playcount / played
        line = "{:<30}{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10.2f}\n".format(source, count, percent, playcount, logpercent, played, playedpercent, ratio)
        f.write(line)
    f.write("\n\n")

def albums_by_type():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>11}{:>10}{:>11}{:>10}{:>11}{:>10}\n".format("by Type", "Count", "%", "Plays", "%", "Played", "%", "Ratio"))
    f.write("-" * 105 + "\n")
    sql = "SELECT albumtype, COUNT(albumid) as TypeCount, SUM(playcount) as PlayCount, SUM(played) as Played FROM album inner join albumtype on " \
          "album.albumtypeid = albumtype.albumtypeid where album.sourceid<>6 GROUP BY albumtype ORDER BY TypeCount desc;"
    results = get_results(sql)

    for r in results:
        albumtype = r[0]
        count = int(r[1])
        percent = 0 if albumcount == 0 else (count/albumcount) * 100
        playcount = int(r[2])
        logpercent = 0 if logcount == 0 else (playcount/logcount) * 100
        played = int(r[3])
        playedpercent = 0 if count == 0 else (played/count) * 100
        ratio = 0 if played == 0 else playcount / played
        line = "{:<30}{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10.2f}\n".format(albumtype, count, percent, playcount, logpercent, played, playedpercent, ratio)

        f.write(line)
    f.write("\n\n")

def albums_by_label():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>11}{:>10}{:>11}{:>10}{:>11}{:>10}\n".format("by Label", "Count", "%", "Plays", "%", "Played", "%", "Ratio"))
    f.write("-" * 105 + "\n")
    sql = "SELECT Label, COUNT(albumid) as TypeCount, SUM(playcount) as PlayCount, SUM(played) as Played FROM album inner join albumtype on " \
          "album.albumtypeid = albumtype.albumtypeid inner join label on album.labelid = label.labelid where Label is not null and albumtype.albumtypeid <> 16 GROUP BY Label ORDER BY TypeCount desc limit 20;"
    results = get_results(sql)

    for r in results:
        label = shorten_by_word(r[0],25)
        count = int(r[1])
        percent = 0 if albumcount == 0 else (count/albumcount) * 100
        playcount = int(r[2])
        logpercent = 0 if logcount == 0 else (playcount/logcount) * 100
        played = int(r[3])
        playedpercent = 0 if count == 0 else (played/count) * 100
        ratio = 0 if played == 0 else playcount / played
        line = "{:<30}{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10.2f}\n".format(label, count, percent, playcount, logpercent, played, playedpercent, ratio)

        f.write(line)
    f.write("\n\n")

def albums_by_retailer():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>11}{:>10}{:>11}{:>10}{:>11}{:>10}\n".format("by Retailer", "Count", "%", "Plays", "%", "Played", "%", "Ratio"))
    f.write("-" * 105 + "\n")
    sql = "select retailers.retailer, count(album.AlbumID) as count, sum(album.playcount) as plays, sum(album.Played) as played " \
          "from album inner join retailers on retailers.retailerid = album.retailerid group by retailers.retailer order by count desc;"
    results = get_results(sql)

    for r in results:
        retailer = r[0]
        count = int(r[1])
        percent = 0 if albumcount == 0 else (count/albumcount) * 100
        playcount = int(r[2])
        logpercent = 0 if logcount == 0 else (playcount/logcount) * 100
        played = int(r[3])
        playedpercent = 0 if count == 0 else (played/count) * 100
        ratio = 0 if played == 0 else playcount / played
        line = "{:<30}{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10.2f}\n".format(retailer, count, percent, playcount, logpercent, played, playedpercent, ratio)
        f.write(line)
    f.write("\n\n")

def albums_by_decade():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>11}{:>10}{:>11}{:>10}{:>11}{:>10}\n".format("by Decade", "Count", "%", "Plays", "%", "Played","%","Ratio"))
    f.write("-" * 105 + "\n")
    sql = "SELECT (yearreleased DIV 10) * 10 as Decade, COUNT(albumid) as TypeCount, SUM(playcount) as PlayCount, sum(played) as Played FROM album " \
          "where album.sourceid<>6 GROUP BY Decade ORDER BY Decade;"

    results = get_results(sql)

    for r in results:
        y = int(r[0])
        count = int(r[1])
        percent = 0 if albumcount == 0 else (count/albumcount) * 100
        playcount = int(r[2])
        logpercent = 0 if logcount == 0 else (playcount/logcount) * 100
        played = int(r[3])
        playedpercent = 0 if count ==0 else (played/count) * 100
        ratio = 0 if played == 0 else playcount / played
        line = "{:<30}{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10.2f}\n".format(y, count, percent, playcount, logpercent, played, playedpercent, ratio)

        f.write(line)
    f.write("\n\n")

def albums_by_year():
    global albumcount
    global logcount
    global albumsplayed

    f.write("{:<30}{:>10}{:>11}{:>10}{:>11}{:>10}{:>11}{:>10}\n".format("by Year of Release", "Count", " ", "Plays", " ", "Played","%", "Ratio"))
    f.write("-" * 105 + "\n")
    sql = "SELECT yearreleased, COUNT(albumid) as TypeCount, SUM(playcount) as PlayCount, Sum(played) as Played FROM album " \
          "WHERE yearreleased >= 2018 and album.sourceid<>6 GROUP BY yearreleased ORDER BY yearreleased;"

    results = get_results(sql)

    for r in results:
        y = int(r[0])
        count = int(r[1])
        percent = 0 if albumcount == 0 else (count/albumcount) * 100
        playcount = int(r[2])
        logpercent = 0 if logcount == 0 else (playcount/logcount) * 100
        played = int(r[3])
        playedpercent = (played/count) * 100
        ratio = 0 if played == 0 else playcount / played
        if y % 10 == 0:
            f.write("-" * 105 + "\n")
        line = "{:<30}{:>10}{:>21}{:>21}{:>10.2f}%{:>10.2f}\n".format(y, count, playcount, played, playedpercent, ratio)

        f.write(line)
    f.write("\n\n")

def albums_by_length():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>11}{:>10}{:>11}{:>10}{:>11}{:>10}\n".format("by Length", "Count", "%", "Plays", "%", "Played","%","Ratio"))
    f.write("-" * 105 + "\n")
    sql = "SELECT ((albumlength/60) DIV 15) * 15 as LengthGroup, COUNT(albumlengths.albumid) as TypeCount, " \
          "SUM(album.playcount) as PlayCount, sum(album.played) as Played " \
          "FROM albumlengths INNER JOIN album on albumlengths.albumid = album.albumid " \
          "where albumlength < 120*60 and album.sourceid<>6 GROUP BY LengthGroup ORDER BY LengthGroup;"

    results = get_results(sql)

    for r in results:
        y = int(r[0])
        count = int(r[1])
        percent = 0 if albumcount == 0 else (count/albumcount) * 100
        playcount = int(r[2])
        logpercent = 0 if logcount == 0 else (playcount/logcount) * 100
        played = int(r[3])
        playedpercent = (played/count) * 100
        ratio = 0 if played == 0 else playcount / played

        tstring = "{} - {} min".format(y, y+14)
        line = "{:<30}{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10.2f}\n".format(tstring, count, percent, playcount, logpercent, played, playedpercent, ratio)

        f.write(line)

        if (y + 15) % 60 == 0:
            f.write("-" * 105 + "\n")

    sql = "SELECT ((albumlength/60) DIV 15) * 15 as LengthGroup, COUNT(albumlengths.albumid) as TypeCount, " \
          "SUM(album.playcount) as PlayCount, sum(album.played) as Played " \
          "FROM albumlengths INNER JOIN album on albumlengths.albumid = album.albumid " \
          "where albumlength >= 120*60 and album.sourceid<>6;"

    results = get_results(sql)

    for r in results:
        y = int(r[0])
        count = int(r[1])
        percent = 0 if albumcount == 0 else (count/albumcount) * 100
        playcount = int(r[2])
        logpercent = 0 if logcount == 0 else (playcount/logcount) * 100
        played = int(r[3])
        playedpercent = (played/count) * 100
        ratio = 0 if played == 0 else playcount / played

        tstring = "{} - {} min".format(y, y+14)
        line = "{:<30}{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10.2f}\n".format("120+ min", count, percent, playcount, logpercent, played, playedpercent, ratio)

        f.write(line)


    f.write("\n\n")

def albums_played_last_14days():
    sql = "select artistcredit, album, logdate from log_history where logdate > (DATE_SUB(CURRENT_DATE, INTERVAL 14 DAY))"

    results = get_results(sql)
    last_log_date = None
    for r in results:
        artistname = shorten_by_word(r[0], 35)
        album = shorten_by_word(r[1], 35)
        logdate = r[2]
        if logdate != last_log_date:
            f.write("\n" + ("-" * 5) + " " + str(logdate) + " " + ("-" * 88) + "\n\n")
        last_log_date = logdate
        line = "{:<40}{:<40}\n".format(artistname.upper(), album)

        f.write(line)
    f.write("\n\n")


def albums_added_last_14days():
    sql = "select artistcredit, album, date(dateadded), source from recent_additions where dateadded > (DATE_SUB(CURRENT_DATE, INTERVAL 14 DAY))"

    results = get_results(sql)
    last_log_date = None
    for r in results:
        artistname = shorten_by_word(r[0], 35)
        album = shorten_by_word(r[1], 35)
        logdate = r[2]
        source = r[3]
        if logdate != last_log_date:
            f.write("\n" + ("-" * 5) + " " + str(logdate) + " " + ("-" * 88) + "\n\n")
        last_log_date = logdate
        line = "{:<40}{:<40}{:<10}\n".format(artistname.upper(), album, source)

        f.write(line)
    f.write("\n\n")

# RE-RIP / RE-IMPORT

def albums_requiring_rerip():
    global albumcount
    global logcount

    f.write("{:<80}{:>10}\n".format("Requiring Re-Rip/Re-Import", "Plays"))
    f.write("-" * 105 + "\n")
    sql = "select artistname, title, count(*) as Plays from log_reimport lr where lr.input is null and lr.requires_rerip = 1 " \
          "group by artistname, title order by plays desc, artistname, title"

    results = get_results(sql)

    for r in results:
        artistname = shorten_by_word(r[0], 35)
        title = shorten_by_word(r[1], 35)
        playcount = int(r[2])
        line = "{:<40}{:<40}{:>10}\n".format(artistname.upper(), title, playcount)

        f.write(line)
    f.write("\n\n")

def albums_requiring_purchase():
    global albumcount
    global logcount

    f.write("{:<80}{:>10}\n".format("Requiring Purchase", "Plays"))
    f.write("-" * 105 + "\n")
    sql = "select artistname, title, count(*) as Plays from log_reimport lr where lr.input is null and lr.requires_rerip is null " \
          "group by artistname, title having Plays >= 3 order by plays desc, artistname, title  LIMIT 10"

    results = get_results(sql)

    for r in results:
        artistname = shorten_by_word(r[0], 35)
        title = shorten_by_word(r[1], 35)
        playcount = int(r[2])
        line = "{:<40}{:<40}{:>10}\n".format(artistname.upper(), title, playcount)

        f.write(line)
    f.write("\n\n")


# TOP 10 ALBUMS

def top_ten_albums_bytime():
    global albumcount
    global logcount

    f.write("{:<80}{:>10}{:>10}\n".format("by Time Played", "Plays", "Hours"))
    f.write("-" * 105 + "\n")
    sql = "select artistname, album, Plays, Points from chart_album_alltime LIMIT 10"

    results = get_results(sql)

    for r in results:
        artistname = r[0][:35]
        title = r[1][:35]
        playcount = int(r[2])
        playedtime = r[3] / 3600
        line = "{:<40}{:<40}{:>10}{:>10.2f}\n".format(artistname.upper(), title, playcount, playedtime)

        f.write(line)
    f.write("\n\n")

def top_ten_albums_bycount():
    global albumcount
    global logcount

    f.write("{:<80}{:>10}{:>10}\n".format("by Plays", "Plays", "Hours"))
    f.write("-" * 105 + "\n")
    sql = "select artistname, album, Plays, Points from chart_album_alltime  order by Plays desc LIMIT 10"

    results = get_results(sql)

    for r in results:
        artistname = shorten_by_word(r[0], 35)
        title = shorten_by_word(r[1], 35)
        playcount = int(r[2])
        playedtime = r[3] / 3600
        line = "{:<40}{:<40}{:>10}{:>10.2f}\n".format(artistname.upper(), title, playcount, playedtime)

        f.write(line)
    f.write("\n\n")

def top_ten_streams_bycount():
    global albumcount
    global logcount

    f.write("{:<80}{:>10}{:>10}\n".format("Streams", "Plays", "Hours"))
    f.write("-" * 105 + "\n")
    sql = "select artistname, album, Plays, Points from chart_streamed_alltime  order by Plays desc LIMIT 10"

    results = get_results(sql)

    for r in results:
        artistname = shorten_by_word(r[0], 35)
        title = shorten_by_word(r[1], 35)
        playcount = int(r[2])
        playedtime = r[3] / 3600
        line = "{:<40}{:<40}{:>10}{:>10.2f}\n".format(artistname.upper(), title, playcount, playedtime)

        f.write(line)
    f.write("\n\n")

def top_ten_albums_last_28days():
    global albumcount
    global logcount

    f.write("{:<80}{:>10}{:>10}\n".format("Last 28 Days", "Plays", "Hours"))
    f.write("-" * 105 + "\n")
    sql = "select `artist`.`ArtistName` AS `ArtistName`,`album`.`Album` AS `Album`," \
          "sum(`albumlengths`.`albumlength`) AS `Points`,count(`log`.`logID`) AS `Plays` " \
          "from ((((`artist` join albumartist on artist.artistid = albumartist.artistid inner join `album` " \
          "on((`albumartist`.`albumID` = `album`.`albumID`))) " \
          "join `albumlengths` on((`album`.`AlbumID` = `albumlengths`.`albumid`))) " \
          "join `log` on((`log`.`AlbumID` = `album`.`AlbumID`))) " \
          "join `albumtype` on((`album`.`AlbumTypeID` = `albumtype`.`AlbumTypeID`))) " \
          "where log.logDate > (DATE_SUB(CURRENT_DATE, INTERVAL 28 DAY)) and album.sourceid<>6 " \
          "group by `artist`.`ArtistID`,`album`.`AlbumID`,`artist`.`ArtistName`,`album`.`Album` " \
          "order by sum(`albumlengths`.`albumlength`) desc limit 10"

    results = get_results(sql)

    for r in results:
        artistname = shorten_by_word(r[0], 35)
        title = shorten_by_word(r[1], 35)
        playcount = int(r[3])
        playedtime = r[2] / 3600
        line = "{:<40}{:<40}{:>10}{:>10.2f}\n".format(artistname.upper(), title, playcount, playedtime)

        f.write(line)
    f.write("\n\n")


# TOP 10 ARTISTS

def top_ten_artists_count():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>11}{:>10}{:>11}{:>10}{:>11}{:>10}\n".format("by Count", "Count", "%", "Plays", "%", "Played", "%", "Ratio"))
    f.write("-" * 105 + "\n")
    sql = "select ArtistName, count(album.AlbumID) as Albums, sum(album.PlayCount) as Plays, sum(album.played) as Played " \
          "from artist inner join albumartist on artist.ArtistID = albumartist.ArtistID " \
          "inner join album on albumartist.albumid = album.albumid " \
          "where album.sourceid<>6 group by artist.ArtistName order by Albums desc limit 10;"

    results = get_results(sql)

    for r in results:
        artistname = shorten_by_word(r[0], 25)
        count = int(r[1])
        percent = 0 if albumcount == 0 else (count/albumcount) * 100
        playcount = int(r[2])
        logpercent = 0 if logcount == 0 else (playcount/logcount) * 100
        played = int(r[3])
        playedpercent = 0 if count == 0 else (played/count) * 100
        ratio = 0 if played == 0 else playcount/played
        line = "{:<30}{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10.2f}\n".format(artistname.upper(), count, percent, playcount, logpercent, played, playedpercent, ratio)

        f.write(line)
    f.write("\n\n")

def top_ten_artists_log():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>11}{:>10}{:>11}{:>10}{:>11}{:>10}\n".format("by Plays", "Count", "%", "Plays", "%", "Played", "%", "Ratio"))
    f.write("-" * 105 + "\n")
    sql = "select artist.ArtistName, count(album.AlbumID) as Albums, sum(album.PlayCount) as Plays, sum(album.played) as Played " \
          "from artist inner join albumartist on artist.artistid = albumartist.artistid " \
          "inner join album on album.albumid = albumartist.albumid " \
          "where album.sourceid<>6 group by artist.ArtistName order by Plays desc limit 10;"

    results = get_results(sql)

    for r in results:
        artistname = shorten_by_word(r[0], 25)
        count = int(r[1])
        percent = 0 if albumcount == 0 else (count/albumcount) * 100
        playcount = int(r[2])
        logpercent = 0 if logcount == 0 else (playcount/logcount) * 100
        played = int(r[3])
        playedpercent = 0 if count == 0 else (played/count) * 100
        ratio = 0 if played == 0 else playcount/played
        line = "{:<30}{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10}{:>10.2f}%{:>10.2f}\n".format(artistname.upper(), count, percent, playcount, logpercent, played, playedpercent, ratio)

        f.write(line)
    f.write("\n\n")

def top_ten_artists_time_played():
    global albumcount
    global logcount

    f.write("{:<31}{:>9}{:>11}\n".format("by Time Played", "Plays", "Hours"))
    f.write("-" * 80 + "\n")
    sql = "select artistname, plays, points / 3600 as hours from chart_artist_alltime order by hours desc limit 10;"

    results = get_results(sql)

    for r in results:
        artistname = shorten_by_word(r[0], 25)
        count = int(r[1])
        time = r[2]
        line = "{:<30}{:>10}{:>11.2f}\n".format(artistname.upper(), count, time)

        f.write(line)
    f.write("\n\n")

def top_ten_artists_time_total():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>11}\n".format("by Time Total", "Count", "Hours"))
    f.write("-" * 80 + "\n")
    sql = "select artistname, count(album.albumid) as albums, sum(albumlength) / 3600 as hours from " \
          "albumlengths inner join album on albumlengths.albumid = album.albumid " \
          "inner join albumartist on album.albumid = albumartist.albumid " \
          "inner join artist on albumartist.artistid = artist.artistid " \
          "where album.sourceid<>6 " \
          "group by artistname order by hours desc limit 10;"

    results = get_results(sql)
    for r in results:
        artistname = shorten_by_word(r[0], 25)
        count = int(r[1])
        time = r[2]
        line = "{:<30}{:>10}{:>11.2f}\n".format(artistname.upper(), count, time)

        f.write(line)

    f.write("\n\n")

def top_ten_artists_28days():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>11}\n".format("Last 28 Days", "Plays", "Hours"))
    f.write("-" * 80 + "\n")
    sql = "select artist.ArtistName, sum(albumlengths.albumlength)/3600 as hours, count(log.logID) as logged " \
          "from log inner join albumlengths on log.AlbumID = albumlengths.AlbumID " \
          "inner join album on album.albumid = albumlengths.albumid " \
          "inner join albumartist on album.albumid = albumartist.albumid " \
          "inner join artist on albumartist.artistid = artist.ArtistID " \
          "where log.logDate > (DATE_SUB(CURRENT_DATE, INTERVAL 28 DAY)) and album.sourceid<>6 " \
          "group by artist.ArtistName order by hours desc limit 10;"

    results = get_results(sql)

    for r in results:
        artistname = shorten_by_word(r[0], 25)
        count = int(r[2])
        time = r[1]
        line = "{:<30}{:>10}{:>11.2f}\n".format(artistname.upper(), count, time)

        f.write(line)
    f.write("\n\n")


# MISSING LOGS

def missing_logs_year(y):
    sql = "select count(*) as Count from log_reimport " \
          "WHERE YEAR(logdate) = {} AND input is null;".format(y)
    result = get_results(sql)
    return result[0][0]

def missing_logs_week(y, w):
    sql = "select count(*) as Count from log_reimport " \
          "WHERE YEAR(logdate) = {} AND (WEEK(logdate) + 1) = {} AND input is null;".format(y, w)
    result = get_results(sql)
    return result[0][0]

def missing_logs_month(y, m):
    sql = "select count(*) as Count from log_reimport " \
          "WHERE YEAR(logdate) = {} AND MONTH(logdate) = {} and input is null;".format(y, m)
    result = get_results(sql)
    return result[0][0]

def missing_logs_date(logdate):
    sql = "select count(*) as Count from log_reimport " \
          "WHERE logdate = '{}' and input is null;".format(logdate)
    result = get_results(sql)
    return result[0][0]


# TIME PERIOD

def monthly_stats():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>10}{:>20}{:>11}{:>11}\n".format("by Month", "Count", "Hrs", "Avg. Len (min)", "Missing", "Total"))
    f.write("-" * 105 + "\n")
    sql = "select * FROM (SELECT * from listen_permonth where (Y>=2018) OR (Y = YEAR(CURRENT_DATE) AND M<>MONTH(CURRENT_DATE)) ORDER BY Y DESC, M DESC LIMIT 24) rr ORDER BY Y,M ASC;"

    results = get_results(sql)

    for r in results:
        y = str(r[0]) + "-" + str(r[1]).zfill(2)
        missing = missing_logs_month(r[0],r[1])
        count = int(r[3])
        logtime = r[2]
        avg = ((logtime * 60) / count)
        total = count + missing
        line = "{:<30}{:>10}{:>10.2f}{:>20.2f}{:>11}{:>11}\n".format(y, count, logtime, avg, missing, total)

        f.write(line)

        if r[1] == 12:
            f.write("-" * 105 + "\n")

    f.write("\n\n")

def weekly_stats():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>10}{:>20}{:>11}{:>11}\n".format("by Week", "Count", "Hrs", "Avg. Len (min)", "Missing", "Total"))
    f.write("-" * 105 + "\n")
    sql = "select * FROM (SELECT * from listen_perweek where (Y>=2018) OR (Y = YEAR(CURRENT_DATE) AND W<>WEEK(CURRENT_DATE)+1) ORDER BY Y DESC, W DESC LIMIT 26) rr ORDER BY Y,W ASC;"

    results = get_results(sql)

    for r in results:
        y = str(r[0]) + "-" + str(r[1]).zfill(2)
        missing = missing_logs_week(r[0],r[1])
        count = int(r[3])
        logtime = r[2]
        avg = ((logtime * 60) / count)
        total = count + missing
        line = "{:<30}{:>10}{:>10.2f}{:>20.2f}{:>11}{:>11}\n".format(y, count, logtime, avg, missing, total)

        f.write(line)

        if r[1] % 13 == 0:
            f.write("-" * 105 + "\n")

    f.write("\n\n")

def annual_stats():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>10}{:>20}{:>11}{:>11}\n".format("Annual Stats", "Count", "Hrs", "Avg. Len (min)", "Missing", "Total"))
    f.write("-" * 105 + "\n")
    sql = "select year(`log`.`logDate`) as Y, sum(`albumlengths`.`albumlength`) / 3600 AS `time`, count(`log`.`logID`) AS `logcount` " \
          "from `log` inner join `albumlengths` on `log`.`AlbumID` = `albumlengths`.`albumid` inner join album on albumlengths.albumid = album.albumid " \
          "where album.sourceid <> 6 group by Y order by Y"
    results = get_results(sql)

    for r in results:
        y = r[0]
        missing = missing_logs_year(y)
        count = int(r[2])
        logtime = r[1]
        avg = ((logtime * 60) / count)
        total = count + missing
        line = "{:<30}{:>10}{:>10.2f}{:>20.2f}{:>11}{:>11}\n".format(y, count, logtime, avg, missing, total)

        f.write(line)

        if r[1] % 13 == 0:
            f.write("-" * 105 + "\n")

    f.write("\n\n")

def thisweek_stats():
    global albumcount
    global logcount

    f.write("{:<30}{:>10}{:>10}{:>20}{:>11}{:>11}\n".format("This Week", "Count", "Hrs", "Avg. Len (min)", "Missing", "Total"))
    f.write("-" * 105 + "\n")
    sql = "select `log`.`logDate`, sum(`albumlengths`.`albumlength`) / 3600 AS `time`, count(`log`.`logID`) AS `logcount` " \
          "from `log` inner join `albumlengths` on `log`.`AlbumID` = `albumlengths`.`albumid` inner join album on albumlengths.albumid = album.albumid " \
          "where (year(logDate) = year(CURRENT_DATE)) and (week(logDate) = week(CURRENT_DATE) and album.sourceid<>6) group by logDate order by logDate"
    results = get_results(sql)

    for r in results:
        logdate = r[0].strftime("%Y-%m-%d")
        missing = missing_logs_date(logdate)
        count = int(r[2])
        logtime = r[1]
        avg = ((logtime * 60) / count)
        total = count + missing
        line = "{:<30}{:>10}{:>10.2f}{:>20.2f}{:>11}{:>11}\n".format(logdate, count, logtime, avg, missing, total)

        f.write(line)

        if r[1] % 13 == 0:
            f.write("-" * 105 + "\n")

    f.write("\n\n")


# GENERAL

def total_albums():
    sql = "SELECT COUNT(albumid) FROM album where SourceID<>6;"
    results = get_results(sql)
    return results[0][0]

def streamed_albums():
    sql = "SELECT COUNT(albumid) FROM album where SourceID=6;"
    results = get_results(sql)
    return results[0][0]

def total_artists():
    sql = "SELECT COUNT(artistid) FROM artist;"
    results = get_results(sql)
    return results[0][0]

def total_size():
    sql = "SELECT GB FROM collection_size;"
    results = get_results(sql)
    return results[0][0]

def total_logs():
    sql = "SELECT SUM(playcount) FROM album where SourceID<>6;"
    results = get_results(sql)
    return results[0][0]

def total_streams():
    sql = "SELECT SUM(playcount) FROM album where SourceID=6;"
    results = get_results(sql)
    return results[0][0]

def total_albums_played():
    sql = "SELECT SUM(played) FROM album where sourceid<>6;"
    results = get_results(sql)
    return results[0][0]

def total_time():
    sql = "SELECT SUM(tracklength) FROM tracklengths inner join album on tracklengths.albumid = album.albumid " \
          "where album.sourceid<>6;"
    results = get_results(sql)
    return results[0][0]

def total_excl_bonus():
    sql = "SELECT SUM(tracklength) FROM tracklengths inner join album on tracklengths.albumid = album.albumid " \
          "where album.sourceid<> 6 and BonusTrack = 0;"
    results = get_results(sql)
    return results[0][0]

def get_media_count(physical):
    if physical:
        criteria = "<= 3"
    else:
        criteria = "BETWEEN 4 and 5"

    sql = "SELECT COUNT(albumid) as AlbumCount FROM album where SourceID {};".format(criteria)
    results = get_results(sql)
    return results[0][0]



def main():
    global albumcount
    global albumsplayed
    global logcount

    openreportfile()

    albumcount = total_albums()
    artistcount = total_artists()
    streamcount = streamed_albums()

    logcount = total_logs()
    albumsplayed = total_albums_played()
    albumsstreamed = total_streams()
    physical_albums = get_media_count(True)
    digital_albums = get_media_count(False)

    f.write(("*" * 105) + "\n")
    f.write("GENERAL\n")
    f.write("*" * 105 + "\n\n")


    f.write("{:<30}{:>10}\n".format("Total Albums:", albumcount))
    f.write("{:<30}{:>10}\n\n".format("Total Artists:", artistcount))

    f.write("{:<30}{:>10}{:>10.2f}%\n".format("Physical Albums:", physical_albums, (physical_albums/albumcount)*100))
    f.write("{:<30}{:>10}{:>10.2f}%\n\n".format("Digital Albums:", digital_albums, (digital_albums/albumcount)*100))

    f.write("{:<30}{:>10}\n".format("Total Plays:", logcount))
    f.write("{:<30}{:>10}{:>10.2f}%\n".format("Unique Albums Played:", albumsplayed, (albumsplayed/albumcount)*100))
    f.write("{:<30}{:>10.2f}\n\n".format("Ratio:", (logcount/albumsplayed)))

    streamed_album_pc = streamcount / (albumcount + streamcount) * 100
    total_streams_pc = albumsstreamed / (logcount + albumsstreamed) * 100

    f.write("{:<30}{:>10}{:>10.2f}%\n".format("Streamed Albums:", streamcount, streamed_album_pc))
    f.write("{:<30}{:>10}{:>10.2f}%\n\n".format("Total Streams:", albumsstreamed, total_streams_pc))


    f.write("{:<30}{:>10.2f}\n\n".format("Total Size (GB):", total_size()))

    f.write("{:<30}{:>10.2f}\n".format("Total Time (hrs):", total_time() / 3600))
    f.write("{:<30}{:>10.2f}\n\n".format("Excl. Bonus (hrs):", total_excl_bonus() / 3600))

    f.write("\n\n")

    f.write("\n\n" + ("*" * 105) + "\n")
    f.write("TIME PERIOD\n")
    f.write("*" * 105 + "\n\n")

    annual_stats()
    monthly_stats()
    weekly_stats()
    thisweek_stats()

    f.write("\n\n" + ("*" * 105) + "\n")
    f.write("ALBUMS\n")
    f.write("*" * 105 + "\n\n")

    albums_by_format()
    albums_by_type()
    albums_by_decade()
    albums_by_year()
    albums_by_label()
    albums_by_retailer()
    albums_by_length()

    f.write("\n\n" + ("*" * 105) + "\n")
    f.write("TOP 10 ARTISTS\n")
    f.write("*" * 105 + "\n\n")

    top_ten_artists_count()
    top_ten_artists_log()
    top_ten_artists_time_total()
    top_ten_artists_time_played()
    top_ten_artists_28days()


    f.write("\n\n" + ("*" * 105) + "\n")
    f.write("TOP TEN ALBUMS\n")
    f.write("*" * 105 + "\n\n")

    top_ten_albums_bytime()
    top_ten_albums_bycount()
    top_ten_albums_last_28days()
    top_ten_streams_bycount()


    f.write("\n\n" + ("*" * 105) + "\n")
    f.write("RE-RIP / RE-IMPORT\n")
    f.write("*" * 105 + "\n\n")

    albums_requiring_rerip()

    f.write("\n\n" + ("*" * 105) + "\n")
    f.write("NEW ADDITIONS\n")
    f.write("*" * 105 + "\n\n")

    albums_added_last_14days()


    f.write("\n\n" + ("*" * 105) + "\n")
    f.write("HISTORY\n")
    f.write("*" * 105 + "\n\n")

    albums_played_last_14days()

    f.flush()
    f.close()

if __name__ == '__main__':
    main()
