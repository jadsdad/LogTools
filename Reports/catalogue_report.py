import MySQLdb as MariaDB
import io
import sys
from pathlib import Path
from datetime import date

conn = MariaDB.connect(db='catalogue', use_unicode=True, charset='utf8')

f = None

def openreportfile():
    global f
    f = io.open(str(Path.home()) + "/Charts/Collection.txt", "w", encoding='utf-8')


def add_relationships(artistid, isgroup):
    isgroup = isgroup == b'\x01'
    field = 'child' if isgroup else 'parent'
    sql = "select relationship.artistid_{0}, artist.ArtistName, relationship.startdate, relationship.enddate " \
          "from relationship inner join artist on relationship.artistid_{1} = artist.ArtistID " \
          "where artistid_{0} = {2} order by ArtistName, startdate".format(field,
                                                                           'child' if field == 'parent' else 'parent',
                                                                           artistid)
    c = conn.cursor()
    rowcount = c.execute(sql)
    previousrelationship = None
    rowindex = 1
    if rowcount > 0:
        f.write("-" * 155)
        rel_header = "See also:" if isgroup else "Member of: "
        rows = c.fetchall()
        for r in rows:
            if r[1] == previousrelationship:
                if r[3] is not None:
                    f.write(", {}-{}".format("" if r[2] is None else r[2],
                                               "" if r[3] is None else r[3]))
                else:
                    f.write(", {}-".format(r[2]))
            else:
                if r[3] is not None:
                    f.write("\n{:<20}{} - {}-{}".format(rel_header if rowindex == 1 else "",
                                                        r[1].upper(), "" if r[2] is None else r[2],
                                                        "" if r[3] is None else r[3]))
                else:
                    f.write("\n{:<20}{}".format(rel_header if rowindex == 1 else "", r[1].upper()))
            previousrelationship = r[1]
            rowindex += 1
        f.write("\n")

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

def add_header():
    linestr = "{:<20}{:<12}{:<50}{:<30}{:<10}{:>10}{:>5}{:>5}{:>5}{:>5}\n".format(
        "Type", "Year", "Album", "Label", "Source", "Length", "P", "D", "T", "B")

    f.write(linestr)

def add_credits(creditslist):
    index = 1
    f.write("=" * 155 + "\n")
    for c in creditslist[1:len(creditslist)]:
        f.write("({}) {}\n".format(index, c))
        index += 1


def main():
    openreportfile()

    f.write("COLLECTION AS OF {}\n\n".format(date.today().strftime("%Y-%m-%d")))

    sql = "SELECT * from albumlist;"
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()

    currentartist = ""
    currenttype = ""
    creditslist = [None]

    for r in rows:

        isgroup, artistid, artist, albumtype, yearreleased, album, label, source, \
        albumlength, playcount, lastplayed, discs, tracks, bonus, artistcredit = r[1:16]


        album = shorten_by_word(album, 45)
        label = shorten_by_word(label, 25)

        if artist != currentartist:
            if len(creditslist) > 1:
                add_credits(creditslist)
            creditslist = [None]
            f.write("=" * 155 + "\n\n\n")
            f.write("=" * 155 + "\n")
            f.write(artist.upper() + "\n")
            add_relationships(artistid, isgroup)
            currenttype = ""
            f.write("-" * 155+ "\n")
            add_header()
            #f.write("-" * 155+ "\n")

        if (albumtype != currenttype):
            f.write("-" * 155+ "\n")

        if artistcredit != artist:
            if artistcredit not in creditslist:
                creditslist.append(artistcredit)
            creditindex = creditslist.index(artistcredit)
            album += " ({})".format(creditindex)

        linestr = "{:<20}{:<10}{:<2}{:<50}{:<30}{:<10}{:>10.0f}{:>5}{:>5}{:>5}{:>5}\n".format("" if currenttype == albumtype else albumtype,
                                                                                    yearreleased, "*" if playcount > 0 else " ", album, 'NULL' if label is None else label, source, albumlength / 60,
                                                                                    playcount, discs, tracks, bonus)

        f.write(linestr)

        currentartist = artist
        currenttype = albumtype

    if len(creditslist) > 1:
        add_credits(creditslist)


if __name__ == '__main__':
    main()