# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sqlite3_main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_sqlite3_mainWindow(object):
    def setupUi(self, sqlite3_mainWindow):
        sqlite3_mainWindow.setObjectName("sqlite3_mainWindow")
        sqlite3_mainWindow.resize(969, 694)
        self.centralwidget = QtWidgets.QWidget(sqlite3_mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_query = QtWidgets.QPushButton(self.centralwidget)
        self.btn_query.setGeometry(QtCore.QRect(850, 560, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btn_query.setFont(font)
        self.btn_query.setObjectName("btn_query")
        self.lineEdit_commont = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_commont.setGeometry(QtCore.QRect(70, 560, 741, 26))
        self.lineEdit_commont.setObjectName("lineEdit_commont")
        self.label_field_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_field_2.setGeometry(QtCore.QRect(20, 550, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_field_2.setFont(font)
        self.label_field_2.setObjectName("label_field_2")
        self.groupBox_table = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_table.setGeometry(QtCore.QRect(20, 20, 101, 421))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox_table.setFont(font)
        self.groupBox_table.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_table.setObjectName("groupBox_table")
        self.groupBox_field = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_field.setGeometry(QtCore.QRect(130, 20, 131, 371))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox_field.setFont(font)
        self.groupBox_field.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_field.setObjectName("groupBox_field")
        self.tableView_content = QtWidgets.QTableView(self.centralwidget)
        self.tableView_content.setGeometry(QtCore.QRect(280, 50, 541, 411))
        self.tableView_content.setObjectName("tableView_content")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(870, 100, 82, 88))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.widget.setFont(font)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_del = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btn_del.setFont(font)
        self.btn_del.setObjectName("btn_del")
        self.verticalLayout_2.addWidget(self.btn_del)
        self.btn_add = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btn_add.setFont(font)
        self.btn_add.setObjectName("btn_add")
        self.verticalLayout_2.addWidget(self.btn_add)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(130, 410, 138, 32))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioBtn_notall = QtWidgets.QRadioButton(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioBtn_notall.setFont(font)
        self.radioBtn_notall.setObjectName("radioBtn_notall")
        self.horizontalLayout.addWidget(self.radioBtn_notall)
        self.radioBtn_all = QtWidgets.QRadioButton(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioBtn_all.setFont(font)
        self.radioBtn_all.setObjectName("radioBtn_all")
        self.horizontalLayout.addWidget(self.radioBtn_all)
        # sqlite3_mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(sqlite3_mainWindow)
        self.statusbar.setObjectName("statusbar")
        self.menubar = QtWidgets.QMenuBar(sqlite3_mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 969, 23))
        self.menubar.setObjectName("menubar")
        self.menudsfewrfr = QtWidgets.QMenu(self.menubar)
        self.menudsfewrfr.setObjectName("menudsfewrfr")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.actionOpen_File = QtWidgets.QAction(sqlite3_mainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.actionClose_File = QtWidgets.QAction(sqlite3_mainWindow)
        self.actionClose_File.setObjectName("actionClose_File")
        self.actionExit = QtWidgets.QAction(sqlite3_mainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menudsfewrfr.addAction(self.actionOpen_File)
        self.menudsfewrfr.addAction(self.actionClose_File)
        self.menudsfewrfr.addSeparator()
        self.menudsfewrfr.addAction(self.actionExit)
        self.menubar.addAction(self.menudsfewrfr.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(sqlite3_mainWindow)
        QtCore.QMetaObject.connectSlotsByName(sqlite3_mainWindow)

    def retranslateUi(self, sqlite3_mainWindow):
        _translate = QtCore.QCoreApplication.translate
        sqlite3_mainWindow.setWindowTitle(_translate("sqlite3_mainWindow", "Sqlite3"))
        self.btn_query.setText(_translate("sqlite3_mainWindow", "查询"))
        self.label_field_2.setText(_translate("sqlite3_mainWindow", "命令"))
        self.groupBox_table.setTitle(_translate("sqlite3_mainWindow", "表"))
        self.groupBox_field.setTitle(_translate("sqlite3_mainWindow", "字段"))
        self.btn_del.setText(_translate("sqlite3_mainWindow", "删除"))
        self.btn_add.setText(_translate("sqlite3_mainWindow", "添加"))
        self.radioBtn_notall.setText(_translate("sqlite3_mainWindow", "全不选"))
        self.radioBtn_all.setText(_translate("sqlite3_mainWindow", "全选"))
        self.menudsfewrfr.setTitle(_translate("sqlite3_mainWindow", "File"))
        self.menuHelp.setTitle(_translate("sqlite3_mainWindow", "Help"))
        self.actionOpen_File.setText(_translate("sqlite3_mainWindow", "Open File"))
        self.actionClose_File.setText(_translate("sqlite3_mainWindow", "Close File"))
        self.actionExit.setText(_translate("sqlite3_mainWindow", "Exit"))
