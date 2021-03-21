import cv2
import sys
import time
import os

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

import get_face
import face_recognition
# from file_op import File_Operate
# from sqlite3_op import Operate_Sql
from tools.sqlite_func import Sqlite_Func

from ui_src.MainUI import Ui_Face_Recognition_window
from Sqlite_UI import Sqlite_UI


# 主窗口类
class MainWindow(QMainWindow, Ui_Face_Recognition_window):
    # 构造函数
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.sf = Sqlite_Func()

        # self.opsql = Operate_Sql()

        self.timer_camera_test = QtCore.QTimer()  # qt计数器
        self.timer_camera_face = QtCore.QTimer()  # qt计数器

        self.openSqlite = Sqlite_UI()  # 数据库对象
        self.slot_init()

        self.combobox_face_init()  # 初始化下拉列表:人脸数据表
        self.combobox_checkWork_init()  # 初始化下拉列表:考勤数据表

        self.photoNum = 0  # 照片计数
        self.CAM_NUM = 0
        self.pNum = 0  # 照片计数器
        self.photo_transmission = 0  # 图片传输变量
        self.frame_out = 0

        # 启动Facenet模块
        self.face = face_recognition.face()
        self.init_db()

    def init_db(self):
        if os.path.exists("../DB/StudentFaceDB.db") is False:
            os.mkdir("../DB/StudentFaceDB.db")
        if os.path.exists("../DB/StudentCheckWorkDB.db.db") is False:
            os.mkdir("../DB/StudentCheckWorkDB.db.db")

    # 槽初始化
    def slot_init(self):

        self.timer_camera_test.timeout.connect(self.show_frame)

        self.btn_openCamera.clicked.connect(self.opencamera)
        self.btn_takePhoto.clicked.connect(self.take_photo)

        self.btn_refresh.clicked.connect(self.refresh)

        self.btn_train.clicked.connect(self.train)
        self.btn_recogniton.clicked.connect(self.open_recognition_camera)
        self.btn_sqlite.clicked.connect(self.open_sqlite)

    def open_sqlite(self):
        self.openSqlite.show()

    def opencamera(self):
        if self.timer_camera_test.isActive() == False:
            self.cap = cv2.VideoCapture(0)
            flag = self.cap.open(self.CAM_NUM)
            if flag is None:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"摄像头无法打开!",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            self.btn_openCamera.setText("关闭摄像头")
            self.timer_camera_test.start(25)
        else:
            self.btn_openCamera.setText(u"打开摄像头")
            self.timer_camera_test.stop()
            self.lab_frame.setText(u"无图像输入")
            self.cap.release()

    def show_frame(self):
        ret, frame = self.cap.read()
        if frame is None:
            return
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))
        self.photo_transmission = frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        lable = cv2.putText(frame, '-->Camera OK', (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0),
                            thickness=1, lineType=1)
        showFrame = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        self.lab_frame.setPixmap(QtGui.QPixmap.fromImage(showFrame))

    # 拍照
    def take_photo(self):
        '''
        1、从数据库中读取所有文件名
        2、从文件名中选择文件目录作为照片存储地址
        3、调用拍照程序对当前画面进行拍照
        4、更新拍照数量
        '''

        # 如果摄像头没有打开
        if self.btn_openCamera.text() != '关闭摄像头':
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请打开摄像头!",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            face = self.comboBox_face.currentText()
            id = self.comboBox_id.currentText()
            if id == '' or id is None:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请选择学号!",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                name = '{CLASS}#{id}'.format(CLASS=face, id=id)
                name = '../src_img/{name}.jpg'.format(name=name)
                print(name)
                cv2.imwrite(name, self.photo_transmission)

    # 考勤表初始化
    def combobox_checkWork_init(self, checktable=None):
        self.comboBox_checkWork.clear()

        ret = self.sf.check_table(self.sf.DB_STUDENTCHECKWORK_PATH)
        print("DB:{}\ntables:{}\ntable_nmu:{}".format(self.sf.DB_STUDENTCHECKWORK_PATH, ret, len(ret)))

        readlines = len(ret)
        lineindex = 0

        while lineindex < readlines:
            self.comboBox_checkWork.addItem(ret[lineindex])
            lineindex += 1
        if checktable != '' or checktable is None:
            self.comboBox_checkWork.setCurrentText(checktable)
        print('combobox_checkWork_init done\n')

    # 获取人脸数据表
    def combobox_face_init(self, checked_table=None):
        self.comboBox_face.clear()
        ret = self.sf.check_table(self.sf.DB_STUDENTFACE_PATH)
        table_nmu = len(ret)
        print("DB:{}\ntables:{}\ntable_nmu:{}".format(self.sf.DB_STUDENTFACE_PATH, ret, len(ret)))
        readlines = table_nmu
        lineindex = 0

        while lineindex < readlines:
            self.comboBox_face.addItem(ret[lineindex])
            lineindex += 1
        if checked_table != '' or checked_table is None:
            self.comboBox_face.setCurrentText(checked_table)
        print('combobox_face_init done\n')

        # 初始化id列表
        self.combobox_id_init(self.comboBox_face.currentText())

    def combobox_id_init(self, table):
        # if table == "":
        #     return
        # 读取人脸数据库中所有id
        field = []
        field.append("id")
        print('====', table)
        cmd = self.sf.auto_select(table, field)
        print("cmd-->", cmd)
        ret = self.sf.executeCMD(self.sf.DB_STUDENTFACE_PATH, cmd)
        print("ret:", ret)

        self.comboBox_id.clear()
        print(len(ret))
        for i in range(len(ret)):
            self.comboBox_id.addItem(str(ret[i][0]))

    # 刷新显示数据库并且显示id号
    def refresh(self):

        # 获取当前选中表明
        checked_face = self.comboBox_face.currentText()
        checked_cw = self.comboBox_checkWork.currentText()

        print("当前选中：{},{}".format(checked_face, checked_cw))

        self.combobox_face_init(checked_table=checked_face)
        self.combobox_checkWork_init(checktable=checked_cw)

    def train(self):

        ret = QMessageBox.question(self, "Train", "训练过程中，画面无法更新,训练时间随机器性能决定", QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if ret == QMessageBox.Yes:
            get_face.detection()

    # 打开识别摄像头
    def open_recognition_camera(self):

        if self.btn_openCamera.text() == '关闭摄像头':
            msg = QtWidgets.QMessageBox.warning(self, u"警告", u"请先关闭摄像头!",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            ret = QMessageBox.question(self, "Train", "1、启动时间根据设备性能强弱决定\n\n2、程序启动后按下esc退出检测窗口",
                                       QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            if ret == QMessageBox.Yes:
                print('开启摄像头')
                face = self.comboBox_face.currentText()
                cw = self.comboBox_checkWork.currentText()
                self.face.main(face, cw)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit((app.exec_()))
