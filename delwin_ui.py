# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delwin_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_Del(object):
    def setupUi(self, Form_Del):
        Form_Del.setObjectName("Form_Del")
        Form_Del.resize(451, 320)
        self.widget = QtWidgets.QWidget(Form_Del)
        self.widget.setGeometry(QtCore.QRect(40, 30, 381, 271))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lab_delTest = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lab_delTest.setFont(font)
        self.lab_delTest.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lab_delTest.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_delTest.setObjectName("lab_delTest")
        self.verticalLayout.addWidget(self.lab_delTest)
        self.line_delFaceName = QtWidgets.QLineEdit(self.widget)
        self.line_delFaceName.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.line_delFaceName.setFont(font)
        self.line_delFaceName.setObjectName("line_delFaceName")
        self.verticalLayout.addWidget(self.line_delFaceName)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_delconfirm = QtWidgets.QPushButton(self.widget)
        self.btn_delconfirm.setMaximumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btn_delconfirm.setFont(font)
        self.btn_delconfirm.setObjectName("btn_delconfirm")
        self.horizontalLayout.addWidget(self.btn_delconfirm)
        self.btn_delcancel = QtWidgets.QPushButton(self.widget)
        self.btn_delcancel.setMaximumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btn_delcancel.setFont(font)
        self.btn_delcancel.setObjectName("btn_delcancel")
        self.horizontalLayout.addWidget(self.btn_delcancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form_Del)
        QtCore.QMetaObject.connectSlotsByName(Form_Del)

    def retranslateUi(self, Form_Del):
        _translate = QtCore.QCoreApplication.translate
        Form_Del.setWindowTitle(_translate("Form_Del", "Form"))
        self.lab_delTest.setText(_translate("Form_Del", "请输入需要删除的文件夹名"))
        self.btn_delconfirm.setText(_translate("Form_Del", "确定"))
        self.btn_delcancel.setText(_translate("Form_Del", "取消"))

