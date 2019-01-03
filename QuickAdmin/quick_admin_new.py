import platform
import sys

import MySQLdb as MariaDB
from PyQt5 import QtWidgets

from quick_admin_ui import Ui_QuickAdmin


class QuickAdminForm(Ui_QuickAdmin):
    def __init__(self, ui):
        Ui_QuickAdmin.__init__(self)
        self.setupUi(ui)
        self.conn = MariaDB.connect(db='catalogue', use_unicode=True, charset='utf8')
        self.displayCount()

        self.populateArtCombo()
        self.populateAlbCombo()
        self.populateTypeCombo()
        self.populateSourceCombo()
        self.populateLabelCombo()

        self.populateAlbumDetails()
        self.setTrackHeaders()

        self.cmbArt.currentIndexChanged.connect(self.populateAlbCombo)
        self.cmbAlb.currentIndexChanged.connect(self.populateAlbumDetails)
        self.tableTracks.itemChanged.connect(self.updateTrackData)
        self.cmbType.currentIndexChanged.connect(self.updateAlbumType)
        self.cmbLabel.currentIndexChanged.connect(self.updateAlbumLabel)
        self.cmbSource.currentIndexChanged.connect(self.updateSource)
        self.txtEdition.textChanged.connect(self.updateEdition)
        self.cmdSaveLabel.clicked.connect(self.addNewLabel)

        self.labelComboRefreshing = False

    def displayCount(self):
        sql = "SELECT COUNT(*) as NewCount FROM album WHERE albumtypeid=12;"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        row=cursor.fetchone()
        newcount = row[0]
        print("There are currently {} albums set as NEW".format(newcount))

    def updateEdition(self):
        alb_id = self.getSelectedAlbum()
        if self.txtEdition.text() != "":
            sql = "UPDATE album SET comments = %s WHERE albumid = %s;"
            cursor = self.conn.cursor()
            cursor.execute(sql, (self.txtEdition.text(), alb_id, ))
            self.conn.commit()

    def updateAlbumType(self):
        alb_id = self.getSelectedAlbum()
        typeid = int(self.cmbType.itemData(self.cmbType.currentIndex()))
        sql = "UPDATE album SET albumtypeid = %s WHERE albumid = %s;"
        cursor = self.conn.cursor()
        cursor.execute(sql, (typeid, alb_id, ))
        self.conn.commit()

    def updateAlbumLabel(self):
        if not self.labelComboRefreshing:
            alb_id = self.getSelectedAlbum()
            labelid = int(self.cmbLabel.itemData(self.cmbLabel.currentIndex()))
            sql = "UPDATE album SET labelid = %s WHERE albumid = %s;"
            cursor = self.conn.cursor()
            cursor.execute(sql, (labelid, alb_id, ))
            self.conn.commit()

    def updateSource(self):
        alb_id = self.getSelectedAlbum()
        typeid = self.cmbSource.itemData(self.cmbSource.currentIndex())
        typeid = int(typeid) if typeid is not None else None
        if typeid is not None:
            sql = "UPDATE album SET sourceid = %s WHERE albumid = %s;"
            cursor = self.conn.cursor()
            cursor.execute(sql, (typeid, alb_id, ))
            self.conn.commit()

    def updateTrackData(self, item):
        alb_id = self.getSelectedAlbum()
        row = self.tableTracks.currentRow()
        col = self.tableTracks.currentColumn()
        newdata = item.text()

        if row >= 0:
            disc = int(self.tableTracks.item(row, 0).text())
            track = int(self.tableTracks.item(row, 1).text())

            field = None

            if col == 2:
                field = "tracktitle"
            elif col == 4:
                field = "bonustrack"

            if field is not None:
                sql = "UPDATE track SET {} = %s WHERE albumid = %s AND disc = %s AND track = %s;".format(field)
                cursor = self.conn.cursor()
                cursor.execute(sql, (newdata, alb_id, disc, track, ))
                self.conn.commit()

    def setTrackHeaders(self):
        headers = ["Disc", "Track", "Title", "Length", "Bonus"]
        widths = [40, 40, 400, 60, 40]

        for x in range(0, 5):
            self.tableTracks.setHorizontalHeaderItem(x, QtWidgets.QTableWidgetItem(headers[x]))
            self.tableTracks.setColumnWidth(x, widths[x])

    def getSelectedArtist(self):
        if self.cmbArt.itemData(self.cmbArt.currentIndex()) is not None:
            art_id = int(self.cmbArt.itemData(self.cmbArt.currentIndex()))
            return art_id

    def getSelectedAlbum(self):
        if self.cmbAlb.count() > 0:
            alb_id = int(self.cmbAlb.itemData(self.cmbAlb.currentIndex()))
            return alb_id
        else:
            return None

    def setAlbumType(self):
        alb_id = self.getSelectedAlbum()
        c = self.conn.cursor()
        c.execute("SELECT albumtypeid, sourceid, labelid, comments "
                  "from album where albumid=%s;", (alb_id, ))
        typerow = c.fetchone()
        self.cmbType.setCurrentIndex(self.cmbType.findData(typerow[0]))
        self.cmbSource.setCurrentIndex(self.cmbSource.findData(typerow[1]))
        self.cmbLabel.setCurrentIndex(self.cmbLabel.findData(typerow[2]))
        self.txtEdition.setText(typerow[3])

    @staticmethod
    def makeSafe(text):
        return text.replace("'", "''")

    def labelExists(self, label):
        c = self.conn.cursor()
        rowcount = c.execute("SELECT * from label where label = '{}';".format(self.makeSafe(label)))
        return rowcount > 0

    def addNewLabel(self):
        label = self.txtAddNewLabel.text()
        if not self.labelExists(label) and not label == '':
            sql = "INSERT INTO label(label) values ('{}')".format(self.makeSafe(label))
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            self.populateLabelCombo()
            self.txtAddNewLabel.clear()

    def populateArtCombo(self):
        c = self.conn.cursor()
        c.execute("SELECT distinct artistid, artistname from artists_with_new_album;")
        artlist = c.fetchall()
        if artlist is not None:
            for a in artlist:
                self.cmbArt.addItem(a[1], a[0])

    def populateLabelCombo(self):
        current_value = self.cmbLabel.itemData(self.cmbLabel.currentIndex())
        self.labelComboRefreshing = True
        self.cmbLabel.clear()
        c = self.conn.cursor()
        c.execute("SELECT distinct labelid, label from label order by label;")
        artlist = c.fetchall()

        if artlist is not None:
            for a in artlist:
                self.cmbLabel.addItem(a[1], a[0])

        self.cmbLabel.setCurrentIndex(self.cmbLabel.findData(current_value))
        self.labelComboRefreshing = False

    def populateAlbCombo(self):
        art_id = self.getSelectedArtist()
        if art_id is not None:
            c = self.conn.cursor()
            c.execute("SELECT album.albumid, album from album inner join albumartist on album.albumid = albumartist.albumid "
                      "WHERE artistid={} and albumtypeid = 12 order by album;".format(art_id))
            alblist = c.fetchall()
            self.cmbAlb.clear()
            for a in alblist:
                self.cmbAlb.addItem(a[1], a[0])

    def populateTypeCombo(self):
        c = self.conn.cursor()
        c.execute("SELECT * from albumtype order by albumtypeid;")
        typelist = c.fetchall()

        for a in typelist:
            self.cmbType.addItem(a[1], a[0])

    def populateSourceCombo(self):
        c = self.conn.cursor()
        c.execute("SELECT * from source order by sourceid;")
        typelist = c.fetchall()

        for a in typelist:
            self.cmbSource.addItem(a[1], a[0])

    def clearTrackTable(self):
        while self.tableTracks.rowCount() > 0:
            self.tableTracks.removeRow(0)

    def populateAlbumDetails(self):
        alb_id = self.getSelectedAlbum()
        if alb_id is not None:
            self.setAlbumType()
            c = self.conn.cursor()
            c.execute("SELECT disc, track, tracktitle, length, bonustrack from track "
                      "WHERE albumid={} order by disc, track;".format(alb_id))
            tracklist = c.fetchall()
            self.clearTrackTable()
            for t in tracklist:
                rowpos = self.tableTracks.rowCount()
                self.tableTracks.insertRow(rowpos)
                for x in range(0, 5):
                    self.tableTracks.setItem(rowpos, x, QtWidgets.QTableWidgetItem(str(t[x])))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = QuickAdminForm(dialog)
    dialog.show()
    sys.exit(app.exec_())
