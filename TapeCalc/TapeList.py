import MySQLdb as mariadb
from decimal import Decimal
from datetime import timedelta
from pathlib import Path
import io
import sys

conn = mariadb.connect(db='catalogue', use_unicode=True, charset='utf8', read_default_file='~/.my.cnf')

class Side():
    def __init__(self, index, trackfrom, trackto, time):
        self.index = index
        self.trackfrom = trackfrom
        self.trackto = trackto
        self.time = time

class Tape():
    def __init__(self, name, sidelength):
        self.name = name
        self.sidelength = sidelength

def query_db(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_albumlength(albumid):
    sql = "SELECT albumlength FROM albumlengths WHERE albumid={};".format(albumid)
    return float(query_db(sql)[0][0])

def get_tracks(albumid):
    sql = "SELECT tracklength FROM tracklengths WHERE albumid={} AND bonustrack = 0 " \
          "ORDER BY Disc, Track;".format(albumid)
    return query_db(sql)

def get_albums():
    sql = "SELECT album.albumid, artistname, album " \
          "FROM album INNER JOIN albumartist on album.albumid = albumartist.albumid " \
          "INNER JOIN artist on albumartist.artistid = artist.artistid " \
          "WHERE sourceid=4 and albumtypeid<>7 " \
          "and recordedtocassette is null  " \
          "order by SortName, yearreleased, album;"
    return query_db(sql)

def willfit(tracks, sidelength):
    for t in tracks:
        if t[0] > sidelength * 60:
            return False

    return True

def calculate(albumid, tape):
    sides=[]
    tracks = get_tracks(albumid)
    albumlength = get_albumlength(albumid) / 60
    sidetarget = int(albumlength / tape.sidelength) + 1
    minsidelength = (albumlength / sidetarget) * 0.75
    tgtsidelength = (albumlength / sidetarget)
    maxsidelength = tape.sidelength

    will_fit = willfit(tracks, tape.sidelength)

    subtotal = 0
    sidecount = 1
    minside = 9999
    maxside = 0
    trackindex = 0
    starttrack = 1
    waste = 0
    for t in tracks:
        tracklength = t[0] / 60
        if trackindex + 1 < len(tracks):
            readahead = tracks[trackindex + 1][0] / 60
        else:
            readahead = 0

        startnewside = (subtotal > tgtsidelength) or \
            ((subtotal + tracklength) > maxsidelength) or \
                       ((subtotal > minsidelength) and ((subtotal + tracklength) > maxsidelength))

        if startnewside:
            minside = subtotal if subtotal < minside else minside
            maxside = subtotal if subtotal > maxside else maxside
            waste = tape.sidelength - maxside
            sides.append(Side(sidecount, starttrack, trackindex, subtotal))
            sidecount += 1
            subtotal = tracklength
            starttrack = trackindex + 1
        else:
            subtotal += tracklength

        trackindex += 1

    minside = subtotal if subtotal < minside else minside
    maxside = subtotal if subtotal > maxside else maxside
    waste += tape.sidelength - subtotal
    sides.append(Side(sidecount, starttrack, trackindex, subtotal))

    return tape, will_fit, sidecount, albumlength, minside, maxside, maxside - minside, waste, sides

def format_to_MS(minutes):
    if type(minutes) == Decimal:
        minutes = float(minutes)

    mytime = timedelta(minutes=minutes)
    return "{:2d}:{:02d}".format(int(mytime.total_seconds() // 60), int(mytime.total_seconds() % 60))

def generate_report(extension):
    tapes = [Tape("C90", 45 + extension),
             Tape("C60", 30 + extension),
             Tape("C46", 23 + extension)]

    albums = get_albums()
    f = io.open(str(Path.home()) + "/Charts/TapeList.txt", "w", encoding='utf-8')
    lastartist=""
    f.write("{:<40}{:<40}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}\n".format("ARTIST","ALBUM","RT","TAPE","SIDES","MIN","MAX","DIFF","WASTE"))
    f.write("-" * 150 + "\n")
    for a in albums:
        calculations = []
        albumid, artist, title = a[:3]
        for t in tapes:
            calculations.append(calculate(albumid, t))

        least_units = 9999
        least_waste = 9999
        best_tape = None
        alt_tape = None

        for c in calculations:
            tape, will_fit, sidecount, albumlength, minside, maxside, difference, waste, sides = c
            if will_fit and ((sidecount % 2 == 0) or (sidecount == 1)):
                    units = round(sidecount/2)
                    if units < least_units or (units <= least_units and waste <= least_waste):
                        least_units = units if units < least_units else least_units
                        least_waste = waste if waste < least_waste else least_waste
                        best_tape = c



        if artist != lastartist:
            f.write("-" * 150 + "\n")
            f.write(artist.upper() + "\n")
            f.write("-" * 150 + "\n\n")

        lastartist = artist

        for x in [best_tape, alt_tape]:
            if x is not None:
                tape, will_fit, sidecount, albumlength, minside, maxside, difference, waste, sides = best_tape
                f.write("{:<80}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}\n".format(title[:75],
                                                        format_to_MS(albumlength), tape.name, sidecount,
                                                        format_to_MS(minside), format_to_MS(maxside),
                                                        format_to_MS(difference), format_to_MS(waste)))
                if sidecount > 1:
                    f.write("\n")
                    for s in sides:
                        f.write("\t\tSide {} - Tracks {} to {} - {}\n".format(s.index, s.trackfrom, s.trackto, format_to_MS(s.time)))

                f.write("\n")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        extension = float(sys.argv[1])
    else:
        extension = 0.0

    generate_report(extension)