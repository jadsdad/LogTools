# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quick_log.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(629, 381)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.cmbArt = QtWidgets.QComboBox(Dialog)
        self.cmbArt.setGeometry(QtCore.QRect(10, 40, 381, 22))
        self.cmbArt.setObjectName("cmbArt")
        self.cmbAlb = QtWidgets.QComboBox(Dialog)
        self.cmbAlb.setGeometry(QtCore.QRect(10, 90, 381, 22))
        self.cmbAlb.setObjectName("cmbAlb")
        self.logDate = QtWidgets.QDateEdit(Dialog)
        self.logDate.setGeometry(QtCore.QRect(69, 130, 321, 22))
        self.logDate.setObjectName("logDate")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 47, 13))
        self.label_3.setObjectName("label_3")
        self.cmdLog = QtWidgets.QPushButton(Dialog)
        self.cmdLog.setGeometry(QtCore.QRect(10, 170, 381, 23))
        self.cmdLog.setObjectName("cmdLog")
        self.lstLog = QtWidgets.QListWidget(Dialog)
        self.lstLog.setGeometry(QtCore.QRect(10, 210, 381, 161))
        self.lstLog.setMaximumSize(QtCore.QSize(381, 371))
        self.lstLog.setObjectName("lstLog")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(410, 20, 101, 16))
        self.label_4.setObjectName("label_4")
        self.lstHistory = QtWidgets.QListWidget(Dialog)
        self.lstHistory.setGeometry(QtCore.QRect(410, 40, 211, 331))
        self.lstHistory.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lstHistory.setObjectName("lstHistory")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Quick Log"))
        self.label.setText(_translate("Dialog", "Artist:"))
        self.label_2.setText(_translate("Dialog", "Album:"))
        self.label_3.setText(_translate("Dialog", "Log Date:"))
        self.cmdLog.setText(_translate("Dialog", "Log"))
        self.label_4.setText(_translate("Dialog", "Previous Logs:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

