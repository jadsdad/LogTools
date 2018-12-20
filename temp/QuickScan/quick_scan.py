#!/usr/bin/python3

import os
import platform
import sys
import traceback

import MySQLdb as MariaDB
from PyQt5 import QtGui, QtWidgets
from mutagen import oggvorbis, flac

from QuickScan.quick_scan_ui import Ui_Dialog


class QuickLogForm(Ui_Dialog):
    def __init__(self, ui):
        Ui_Dialog.__init__(self)
        self.setupUi(ui)

        if platform.system() == "Linux":
            self.conn = MariaDB.connect(user='simon', passwd='phaedra74',
                                        db='catalogue', use_unicode=True, charset='utf8')
            self.basedir = "/home/simon/Rips/4 - For DB"
        else:
            self.conn = MariaDB.connect(user='root', passwd='3amatBotMfO',
                                        db='catalogue', use_unicode=True, charset='utf8')
            self.basedir = "c:/Builds in Progress/Test"

    @staticmethod
    def isLinux():
        return platform.system() == "Linux"

    def doScan(self):
        extn = ".flac" if self.isLinux() else ".ogg"
        for root, dirs, files in os.walk(self.basedir):
            for f in files:
                if f.endswith(extn):
                    file = os.path.join(root, f)
                    try:
                        f = flac.FLAC(file) if self.isLinux() else oggvorbis.OggVorbis(file)
                        t = f.tags
                        album_artist = t["ALBUMARTIST"][0]
                        album = t["Album"][0]
                        year = str(t["Date"][0])
                        disc = str(t["DISCNUMBER"][0])
                        track = str(t["tracknumber"][0])
                        title = t["title"][0]
                        length_hr = int(f.info.length / 3600)
                        length_min = int((f.info.length - (length_hr * 3600)) / 60)
                        length_sec = int(f.info.length) % 60
                        length = "{:02d}{:02d}{:02d}".format(length_hr, length_min, length_sec)

                        artistid = self.getArtistID(album_artist)
                        albumid = self.getAlbumID(artistid, album, year)

                        self.addHistory("{}: {}".format(album_artist, title))
                        self.insertTrack(albumid, disc, track, title, length)

                    except:
                        print("--- ERROR IN FILE HEADER: " + traceback.format_exc())
        self.lstStatus.insertItem(0, "ALL DONE!")

        if self.isLinux():
            os.system("rsync -a \"/home/simon/Rips/4 - For DB/\" \"/home/simon/Rips/5 - For Archive/\"")
            os.system("rm -rf '/home/simon/Rips/4 - For DB/'")
            os.system("mkdir '/home/simon/Rips/4 - For DB/'")

    def getArtistID(self, album_artist):
        cursor = self.conn.cursor()
        sql = "SELECT artistid FROM artist WHERE artistname=%s;"
        result = cursor.execute(sql, (album_artist,))
        if result == 0:
            cursor.execute("INSERT INTO artist (artistname) VALUES (%s);", (album_artist,))
            self.conn.commit()
            return cursor.lastrowid
        else:
            row = cursor.fetchone()
            return row[0]

    def getAlbumID(self, artistid, album, year):
        cursor = self.conn.cursor()
        sql = "SELECT albumid FROM album WHERE album=%s AND artistid=%s;"
        result = cursor.execute(sql, (album, artistid,))
        if result == 0:
            cursor.execute("INSERT INTO album (album, yearreleased, artistid, albumtypeid, sourceid) "
                           "VALUES (%s,%s,%s,1,1);",
                           (album, year, artistid,))
            self.conn.commit()
            return cursor.lastrowid
        else:
            row = cursor.fetchone()
            return row[0]

    def getTrackID(self, albumid, disc, track):
        cursor = self.conn.cursor()
        sql = "SELECT trackid FROM track WHERE albumid=%s AND disc=%s and track=%s;"
        result = cursor.execute(sql, (albumid, disc, track,))
        if result == 0:
            return 0
        else:
            return cursor.fetchone()[0]

    def insertTrack(self, albumid, disc, track, title, length):
        cursor = self.conn.cursor()
        trackid = self.getTrackID(albumid, disc, track)

        if trackid == 0:
            cursor.execute("INSERT INTO track (albumid, disc, track, tracktitle, "
                           "length) VALUES (%s,%s,%s,%s,%s);", (albumid, disc, track, title, length,))
        else:
            cursor.execute("UPDATE track SET tracktitle = %s, length = %s "
                           "WHERE trackid = %s", (title, length, trackid,))

        self.conn.commit()

    def addHistory(self, message):
        self.lstStatus.insertItem(0, message)
        QtGui.QGuiApplication.processEvents()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = QuickLogForm(dialog)
    dialog.show()
    prog.doScan()

    sys.exit(app.exec_())
