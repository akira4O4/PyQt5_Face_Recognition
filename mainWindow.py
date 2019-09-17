import cv2
from main_ui import Ui_Face_Recognition_window
from addFace_ui import Ui_Form
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from file_op import File_Operate
from sqlite3_op import Operate_Sql
import os


# 添加窗口类
class add_window(QDialog, Ui_Form):
    def __init__(self):
        super(add_window, self).__init__()
        self.setupUi(self)
        self.slotInit()
        self.opsql = Operate_Sql()
        self.opfile = File_Operate()

    def slotInit(self):
        self.btn_cancel.clicked.connect(self.btn_hide)
        self.btn_confirm.clicked.connect(self.btn_addNewFile)
        # 隐藏窗口

    def btn_hide(self):
        self.hide()

    def btn_addNewFile(self):
        '''
        1、触发确认按钮
        2、向数据库添加新名字
        3、创建新文件夹
        '''
        self.line_addFaceName.clear()
        text = self.line_addFaceName.text()
        print(text)
        if len(text) == 0:
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"目录为空",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            newName = self.opsql.CreatSqlStr(text)
            self.opsql.Insert_New_Name(newName)  # 向数据库插入新行
            # self.lab_addTest.setText('添加完成')
            # self.line_addFaceName.clear()
            self.btn_hide()
            ret = self.opfile.Create_File(text)
            if ret:
                msg = QtWidgets.QMessageBox.information(self, u"完成", u"个人文件夹创建成功！",
                                                        buttons=QtWidgets.QMessageBox.Ok,
                                                        defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                msg = QtWidgets.QMessageBox.critical(self, u"失败", u"无法创建个人文件夹",
                                                     buttons=QtWidgets.QMessageBox.Ok,
                                                     defaultButton=QtWidgets.QMessageBox.Ok)


# 主窗口类
class MainWindow(QMainWindow, Ui_Face_Recognition_window):
    # 构造函数
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.timer_camera = QtCore.QTimer()  # qt计数器

        self.photoNum = 0;  # 照片计数
        self.slot_init()
        self.CAM_NUM = 0
        self.openAddWin = add_window()

    # 槽初始化
    def slot_init(self):
        self.btn_openCamera.clicked.connect(self.OpenCamera)
        # self.btn_takePhoto.clicked.connect(self.Take_Photo)
        self.timer_camera.timeout.connect(self.Show_Frame)
        self.btn_addFace.clicked.connect(self.open_Add_Win)

    def OpenCamera(self):

        if self.timer_camera.isActive() == False:
            self.cap = cv2.VideoCapture(0)
            flag = self.cap.open(self.CAM_NUM)
            if flag is None:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"摄像头无法打开!",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            self.btn_openCamera.setText("关闭摄像头")
            self.timer_camera.start(25)
        else:
            self.btn_openCamera.setText(u"打开摄像头")
            self.timer_camera.stop()
            self.lab_frame.setText(u"无图像输入")
            self.cap.release()

    def Show_Frame(self):
        ret, frame = self.cap.read()
        if frame is None:
            print(1)
            return
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        lable = cv2.putText(frame, '-->Camera OK', (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0),
                            thickness=1, lineType=1)
        showFrame = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        self.lab_frame.setPixmap(QtGui.QPixmap.fromImage(showFrame))

    # 打开添加窗口
    def open_Add_Win(self):
        self.openAddWin.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit((app.exec_()))
