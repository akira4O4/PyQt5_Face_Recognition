# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addFace_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(22, 166, 361, 121))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_confirm = QtWidgets.QPushButton(self.widget)
        self.btn_confirm.setMaximumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btn_confirm.setFont(font)
        self.btn_confirm.setObjectName("btn_confirm")
        self.horizontalLayout.addWidget(self.btn_confirm)
        self.btn_cancel = QtWidgets.QPushButton(self.widget)
        self.btn_cancel.setMaximumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.widget1 = QtWidgets.QWidget(Form)
        self.widget1.setGeometry(QtCore.QRect(30, 30, 351, 81))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lab_addTest = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lab_addTest.setFont(font)
        self.lab_addTest.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lab_addTest.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lab_addTest.setObjectName("lab_addTest")
        self.verticalLayout.addWidget(self.lab_addTest)
        self.line_addFaceName = QtWidgets.QLineEdit(self.widget1)
        self.line_addFaceName.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.line_addFaceName.setFont(font)
        self.line_addFaceName.setObjectName("line_addFaceName")
        self.verticalLayout.addWidget(self.line_addFaceName)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_confirm.setText(_translate("Form", "确定"))
        self.btn_cancel.setText(_translate("Form", "取消"))
        self.lab_addTest.setText(_translate("Form", "请添加新用户文件名（不支持中文）"))

