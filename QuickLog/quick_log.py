#!/usr/bin/python3

import platform
import sys

import MySQLdb as MariaDB
from PyQt5 import QtCore, QtWidgets

from quick_log_ui import Ui_Dialog


class QuickLogForm(Ui_Dialog):
    def __init__(self, ui):
        Ui_Dialog.__init__(self)
        self.setupUi(ui)

        self.conn = MariaDB.connect(db='catalogue', use_unicode=True, charset='utf8', read_default_file='~/.my.cnf')
        self.logDate.setDate(QtCore.QDate.currentDate())
        self.populateArtCombo()
        self.populateAlbCombo()

        self.cmbArt.currentIndexChanged.connect(self.populateAlbCombo)
        self.cmbAlb.currentIndexChanged.connect(self.updateHistory)
        self.cmdLog.clicked.connect(self.saveLog)

    def makesafe(self, text):
        return text.replace("'", "''")
    
    def updateHistory(self):
        alb_id = self.getSelectedAlbum()
        c = self.conn.cursor()
        c.execute("SELECT logdate FROM log WHERE albumid=%s ORDER BY logdate DESC;", (alb_id,))
        logs = c.fetchall()

        self.lstHistory.clear()
        for l in logs:
            logdate = l[0]
            self.lstHistory.insertItem(0, str(logdate))

    def populateArtCombo(self):
        c = self.conn.cursor()
        c.execute("SELECT DISTINCT artistcredit from album order by artistcredit;")
        artlist = c.fetchall()

        for a in artlist:
            self.cmbArt.addItem(a[0], a[0])

    def populateAlbCombo(self):
        art_id = self.makesafe(self.getSelectedArtist())
        c = self.conn.cursor()
        c.execute("SELECT albumid, album, yearreleased from album WHERE artistcredit='{}' order by yearreleased, album;".format(art_id))
        alblist = c.fetchall()
        self.cmbAlb.clear()
        for a in alblist:
            self.cmbAlb.addItem(str(a[2]) + " - " + a[1], a[0])

    def getSelectedArtist(self):
        if self.cmbArt.count() > 0:
            art_id = self.cmbArt.itemData(self.cmbArt.currentIndex())
            return art_id
        else:
            return 0

    def getSelectedAlbum(self):
        if self.cmbAlb.count() > 0:
            alb_id = int(self.cmbAlb.itemData(self.cmbAlb.currentIndex()))
            return alb_id
        else:
            return 0

    def saveLog(self):
        alb_id = self.getSelectedAlbum()
        log_date = self.logDate.date()

        sql = "INSERT INTO log (albumid, logdate) VALUES ({},'{}')".format(alb_id, log_date.toString("yyyy-MM-dd"))
        c = self.conn.cursor()
        c.execute(sql)
        self.conn.commit()
        self.addHistory("Logged: " + self.cmbAlb.currentText())
        self.updateHistory()

    def addHistory(self, message):
        self.lstLog.insertItem(0, message)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = QuickLogForm(dialog)

    dialog.show()
    sys.exit(app.exec_())
