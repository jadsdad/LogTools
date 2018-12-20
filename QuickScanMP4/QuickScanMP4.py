#!/usr/bin/python3

import os
import sys

import MySQLdb as MariaDB
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication
from mutagen import mp4

file_path = "C:\\Users\\simon\\Music\\iTunes\\iTunes Media\\Music\\"

class QuickLogForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setObjectName("Form")
        self.resize(278, 233)
        self.setWindowTitle("MP4 Scanner")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label.setObjectName("label")
        self.lstStatus = QtWidgets.QListWidget(self)
        self.lstStatus.setGeometry(QtCore.QRect(10, 30, 256, 192))
        self.lstStatus.setObjectName("lstStatus")

        self.conn = MariaDB.connect(user='root', passwd='3amatBotMfO',
                                    db='catalogue', use_unicode=True, charset='utf8')
        self.basedir = str(QFileDialog.getExistingDirectory(self, "Select Directory", directory=file_path))


        self.show()
        self.doScan()

    def doScan(self):
        extn = ".m4a"
        for root, dirs, files in os.walk(self.basedir):
            for f in files:
                if f.endswith(extn):
                    file = os.path.join(root, f)
                    f = mp4.MP4(file)
                    t = f.tags
                    album_artist = t.get("aART")[0]
                    album = t.get("\xa9alb")[0]
                    year = t.get("\xa9day")[0]

                    if len(year) > 4:
                        year=year[:5]

                    disc = t.get("disk")
                    disc = 1 if disc is None else disc[0][0]
                    track = str(t["trkn"][0][0])
                    title = t["\xa9nam"][0]
                    length_hr = int(f.info.length / 3600)
                    length_min = int((f.info.length - (length_hr * 3600)) / 60)
                    length_sec = int(f.info.length) % 60
                    length = "{:02d}{:02d}{:02d}".format(length_hr, length_min, length_sec)

                    artistid = self.getArtistID(album_artist)
                    albumid = self.getAlbumID(artistid, album, year)

                    self.addHistory("{}: {}".format(album_artist, title))
                    self.insertTrack(albumid, disc, track, title, length)

        self.lstStatus.insertItem(0, "ALL DONE!")

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
            cursor.execute("INSERT INTO album (album, yearreleased, artistid, albumtypeid) "
                           "VALUES (%s,%s,%s,12);",
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
    app = QApplication(sys.argv)
    prog = QuickLogForm()
    sys.exit(app.exec_())
