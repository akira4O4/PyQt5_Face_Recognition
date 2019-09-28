# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addFace_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_add(object):
    def setupUi(self, Form):
        Form.setObjectName("addFaceWin")
        Form.resize(454, 285)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(22, 30, 401, 231))
        self.widget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lab_addTest = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lab_addTest.setFont(font)
        self.lab_addTest.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lab_addTest.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_addTest.setObjectName("lab_addTest")
        self.verticalLayout.addWidget(self.lab_addTest)
        self.line_addFaceName = QtWidgets.QLineEdit(self.widget)
        self.line_addFaceName.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.line_addFaceName.setFont(font)
        self.line_addFaceName.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.line_addFaceName.setObjectName("line_addFaceName")
        self.verticalLayout.addWidget(self.line_addFaceName)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_confirm = QtWidgets.QPushButton(self.widget)
        self.btn_confirm.setMaximumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btn_confirm.setFont(font)
        self.btn_confirm.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_confirm.setObjectName("btn_confirm")
        self.horizontalLayout.addWidget(self.btn_confirm)
        self.btn_cancel = QtWidgets.QPushButton(self.widget)
        self.btn_cancel.setMaximumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "添加"))
        self.lab_addTest.setText(_translate("Form", "请添加新用户文件名（不支持中文）"))
        self.btn_confirm.setText(_translate("Form", "确定"))
        self.btn_cancel.setText(_translate("Form", "取消"))

