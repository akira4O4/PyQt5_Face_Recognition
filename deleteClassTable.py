# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deleteClassTable.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DelClassTable(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(498, 250)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 30, 436, 166))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lab_addTest_8 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lab_addTest_8.sizePolicy().hasHeightForWidth())
        self.lab_addTest_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lab_addTest_8.setFont(font)
        self.lab_addTest_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lab_addTest_8.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_addTest_8.setObjectName("lab_addTest_8")
        self.verticalLayout_2.addWidget(self.lab_addTest_8)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lab_addTest_6 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lab_addTest_6.sizePolicy().hasHeightForWidth())
        self.lab_addTest_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lab_addTest_6.setFont(font)
        self.lab_addTest_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lab_addTest_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_addTest_6.setObjectName("lab_addTest_6")
        self.horizontalLayout.addWidget(self.lab_addTest_6)
        self.line_profession = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_profession.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_profession.sizePolicy().hasHeightForWidth())
        self.line_profession.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.line_profession.setFont(font)
        self.line_profession.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.line_profession.setObjectName("line_profession")
        self.horizontalLayout.addWidget(self.line_profession)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lab_addTest_7 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lab_addTest_7.sizePolicy().hasHeightForWidth())
        self.lab_addTest_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lab_addTest_7.setFont(font)
        self.lab_addTest_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lab_addTest_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_addTest_7.setObjectName("lab_addTest_7")
        self.horizontalLayout_3.addWidget(self.lab_addTest_7)
        self.line_class = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_class.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_class.sizePolicy().hasHeightForWidth())
        self.line_class.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.line_class.setFont(font)
        self.line_class.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.line_class.setObjectName("line_class")
        self.horizontalLayout_3.addWidget(self.line_class)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_confirm = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_confirm.sizePolicy().hasHeightForWidth())
        self.btn_confirm.setSizePolicy(sizePolicy)
        self.btn_confirm.setMaximumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btn_confirm.setFont(font)
        self.btn_confirm.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_confirm.setObjectName("btn_confirm")
        self.horizontalLayout_2.addWidget(self.btn_confirm)
        self.btn_cancel = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_cancel.sizePolicy().hasHeightForWidth())
        self.btn_cancel.setSizePolicy(sizePolicy)
        self.btn_cancel.setMaximumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_2.addWidget(self.btn_cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "删除班级表"))
        self.lab_addTest_8.setText(_translate("Form", "删除班级表"))
        self.lab_addTest_6.setText(_translate("Form", "院系"))
        self.lab_addTest_7.setText(_translate("Form", "班级"))
        self.btn_confirm.setText(_translate("Form", "确定"))
        self.btn_cancel.setText(_translate("Form", "取消"))
