# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quick_admin.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QuickAdmin(object):
    def setupUi(self, QuickAdmin):
        QuickAdmin.setObjectName("QuickAdmin")
        QuickAdmin.resize(640, 641)
        self.tableTracks = QtWidgets.QTableWidget(QuickAdmin)
        self.tableTracks.setGeometry(QtCore.QRect(10, 90, 621, 341))
        self.tableTracks.setAlternatingRowColors(True)
        self.tableTracks.setColumnCount(5)
        self.tableTracks.setObjectName("tableTracks")
        self.tableTracks.setRowCount(0)
        self.cmbArt = QtWidgets.QComboBox(QuickAdmin)
        self.cmbArt.setGeometry(QtCore.QRect(60, 20, 281, 22))
        self.cmbArt.setObjectName("cmbArt")
        self.cmbAlb = QtWidgets.QComboBox(QuickAdmin)
        self.cmbAlb.setGeometry(QtCore.QRect(60, 50, 281, 22))
        self.cmbAlb.setObjectName("cmbAlb")
        self.label = QtWidgets.QLabel(QuickAdmin)
        self.label.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(QuickAdmin)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 47, 13))
        self.label_2.setObjectName("label_2")
        self.cmbType = QtWidgets.QComboBox(QuickAdmin)
        self.cmbType.setGeometry(QtCore.QRect(120, 440, 211, 22))
        self.cmbType.setObjectName("cmbType")
        self.label_3 = QtWidgets.QLabel(QuickAdmin)
        self.label_3.setGeometry(QtCore.QRect(10, 440, 101, 16))
        self.label_3.setObjectName("label_3")
        self.cmbSource = QtWidgets.QComboBox(QuickAdmin)
        self.cmbSource.setGeometry(QtCore.QRect(120, 470, 211, 22))
        self.cmbSource.setObjectName("cmbSource")
        self.label_4 = QtWidgets.QLabel(QuickAdmin)
        self.label_4.setGeometry(QtCore.QRect(10, 470, 101, 16))
        self.label_4.setObjectName("label_4")
        self.txtEdition = QtWidgets.QLineEdit(QuickAdmin)
        self.txtEdition.setGeometry(QtCore.QRect(120, 560, 211, 20))
        self.txtEdition.setObjectName("txtEdition")
        self.label_6 = QtWidgets.QLabel(QuickAdmin)
        self.label_6.setGeometry(QtCore.QRect(10, 560, 101, 16))
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(QuickAdmin)
        self.label_5.setGeometry(QtCore.QRect(10, 500, 101, 16))
        self.label_5.setObjectName("label_5")
        self.cmbLabel = QtWidgets.QComboBox(QuickAdmin)
        self.cmbLabel.setGeometry(QtCore.QRect(120, 500, 211, 22))
        self.cmbLabel.setObjectName("cmbLabel")
        self.label_7 = QtWidgets.QLabel(QuickAdmin)
        self.label_7.setGeometry(QtCore.QRect(10, 530, 101, 16))
        self.label_7.setObjectName("label_7")
        self.txtAddNewLabel = QtWidgets.QLineEdit(QuickAdmin)
        self.txtAddNewLabel.setGeometry(QtCore.QRect(120, 530, 211, 20))
        self.txtAddNewLabel.setObjectName("txtAddNewLabel")
        self.cmdSaveLabel = QtWidgets.QPushButton(QuickAdmin)
        self.cmdSaveLabel.setGeometry(QtCore.QRect(340, 530, 101, 24))
        self.cmdSaveLabel.setObjectName("cmdSaveLabel")
        self.txtAddNewLabel.setEnabled(False)
        self.cmdSaveLabel.setEnabled(False)
        self.retranslateUi(QuickAdmin)
        QtCore.QMetaObject.connectSlotsByName(QuickAdmin)

    def retranslateUi(self, QuickAdmin):
        _translate = QtCore.QCoreApplication.translate
        QuickAdmin.setWindowTitle(_translate("QuickAdmin", "Quick Admin"))
        self.label.setText(_translate("QuickAdmin", "Artist:"))
        self.label_2.setText(_translate("QuickAdmin", "Title:"))
        self.label_3.setText(_translate("QuickAdmin", "Type:"))
        self.label_4.setText(_translate("QuickAdmin", "Source"))
        self.label_6.setText(_translate("QuickAdmin", "Edition Notes:"))
        self.label_5.setText(_translate("QuickAdmin", "Label"))
        self.label_7.setText(_translate("QuickAdmin", "Add New Label:"))
        self.cmdSaveLabel.setText(_translate("QuickAdmin", "Save + Refresh"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QuickAdmin = QtWidgets.QDialog()
    ui = Ui_QuickAdmin()
    ui.setupUi(QuickAdmin)
    QuickAdmin.show()
    sys.exit(app.exec_())

