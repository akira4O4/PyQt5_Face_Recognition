import cv2
import sys
import os
import get_face
import tensorflow as tf
from PyQt5.QtWidgets import *
from MainUI import Ui_Face_Recognition_window
from addStudent import Ui_Form_Student
from delwin_ui import Ui_Form_Del
from addClassTable import Ui_AddClassTable
from deleteClassTable import Ui_DelClassTable
from help import Ui_help
from prompt import Ui_For_prompt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from file_op import File_Operate
from sqlite3_op import Operate_Sql
import face_recognition
import time
from scipy import misc
import numpy as np
import os
import facenet
import align.detect_face


# 添加删除窗口
class del_window(QDialog, Ui_Form_Del):
    def __init__(self):
        super(del_window, self).__init__()
        self.setupUi(self)
        self.SlotInit()
        self.opsql = Operate_Sql()
        self.opfile = File_Operate()
        self.line_delFaceName.clear()

    def SlotInit(self):
        self.btn_delcancel.clicked.connect(self.btn_hide)
        self.btn_delconfirm.clicked.connect(self.btn_DelFile)

    def btn_hide(self):
        self.hide()

    def btn_DelFile(self):
        '''
        读取字符串
        删除数据库对应行
        删除对应文件
        :return:
        '''
        text = self.line_delFaceName.text()
        flag = self.opsql.Select_Same_Name(text)
        if flag is False:  # 如果数据库不存在这个目录
            msg = QtWidgets.QMessageBox.warning(self, u"警告", u"不存在这个用户",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)

        else:
            # 从本地删除src_img文件
            if os.path.exists('../src_img/' + text + '.jpg') == True:
                os.remove('../src_img/' + text + '.jpg')

            # 从本地删除emb_img文件
            if os.path.exists('../emb_img/' + text + '.jpg') == True:
                os.remove('../emb_img/' + text + '.jpg')

            self.opsql.Delete_File_Name(text)  # 从数据库中删除这个文件名
            msg = QtWidgets.QMessageBox.information(self, u"完成", u"删除完成！",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)

            self.line_delFaceName.clear()
            self.btn_hide()  # 隐藏窗口


# 删除班级表
class DelClassTable(QDialog, Ui_DelClassTable):
    def __init__(self):
        super(DelClassTable, self).__init__()
        self.setupUi(self)
        self.initslot()
        self.opsql = Operate_Sql()
        self.opfile = File_Operate()
        self.line_profession.clear()
        self.line_class.clear()
        # 初始化信号槽

    def initslot(self):
        self.btn_cancel.clicked.connect(self.btn_hide)
        self.btn_confirm.clicked.connect(self.confirm)

    def btn_hide(self):
        self.hide()

    def confirm(self):
        # 获取院系班级
        profession = self.line_profession.text()
        class_ = self.line_class.text()
        flag = self.opsql.delete_pc_table(profession, class_)
        self.line_profession.clear()
        self.line_class.clear()
        if flag:
            print("完成")
            msg = QtWidgets.QMessageBox.information(self, u"完成", u"删除成功！",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            time.sleep(0.2)
            self.hide()

        else:
            print('失败')
            msg = QtWidgets.QMessageBox.warning(self, u"警告", u"不存在这个表，请更改",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)


# 添加班级表
class AddClassTable(QDialog, Ui_AddClassTable):
    def __init__(self):
        super(AddClassTable, self).__init__()
        self.setupUi(self)
        self.initslot()
        self.opsql = Operate_Sql()
        self.opfile = File_Operate()
        self.line_profession.clear()
        self.line_class.clear()

    # 初始化信号槽
    def initslot(self):
        self.btn_cancel.clicked.connect(self.btn_hide)
        self.btn_confirm.clicked.connect(self.confirm)

    def btn_hide(self):
        self.hide()

    def confirm(self):
        # 获取院系班级
        profession = self.line_profession.text()
        class_ = self.line_class.text()
        flag = self.opsql.create_new_pc_table(profession, class_)
        self.line_profession.clear()
        self.line_class.clear()
        if flag:
            print("完成")
            msg = QtWidgets.QMessageBox.information(self, u"完成", u"个人文件夹创建成功！",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            time.sleep(0.3)
            self.hide()

        else:
            print('失败')
            msg = QtWidgets.QMessageBox.warning(self, u"警告", u"存在相同表名，请更改",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)


# 添加窗口类
class AddStudent(QDialog, Ui_Form_Student):
    def __init__(self):
        super(AddStudent, self).__init__()
        self.setupUi(self)
        self.slotInit()
        self.opsql = Operate_Sql()
        self.opfile = File_Operate()
        self.combobox_init()

    def slotInit(self):
        self.btn_cancel.clicked.connect(self.btn_hide)
        self.btn_confirm.clicked.connect(self.btn_add_new_student)
        # 隐藏窗口

    def btn_hide(self):
        self.hide()

    # 初始化班级列表
    def combobox_init(self):
        table_name, table_nmu = self.opsql.select_all_table()
        readlines = table_nmu
        lineindex = 0
        while lineindex < readlines:
            row = table_name[lineindex]  #
            self.SelectClass.addItem(table_name[lineindex])
            lineindex += 1

    def btn_add_new_student(self):
        student_info = []
        proclass = self.SelectClass.currentText()
        lable = self.line_addLabel.text()
        name = self.line_addName.text()
        sex = self.line_addSex.text()
        id = self.line_addId.text()

        student_info.append(lable)
        student_info.append(name)
        student_info.append(sex)
        student_info.append(id)
        student_info.append(proclass)

        # 检查学号是否唯一存在
        flag = self.opsql.insert_new_student(student_info)
        if flag:
            msg = QtWidgets.QMessageBox.information(self, u"完成", u"添加个人信息完成！",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            self.line_addLabel.clear()
            self.line_addName.clear()
            self.line_addSex.clear()
            self.line_addId.clear()
        else:
            msg = QtWidgets.QMessageBox.warning(self, u"警告", u"存在相学号，请更改",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)


# 提示窗口
class HelpWindow(QDialog, Ui_help):
    def __init__(self):
        super(HelpWindow, self).__init__()
        self.setupUi(self)


# 主窗口类
class MainWindow(QMainWindow, Ui_Face_Recognition_window):
    # 构造函数
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.DB_Path = '../DB/FileNameDB.db'
        self.sqlStr_SelectAll = "select * from fileName;"

        self.opsql = Operate_Sql()
        self.opfile = File_Operate()

        self.timer_camera_test = QtCore.QTimer()  # qt计数器
        self.timer_camera_face = QtCore.QTimer()  # qt计数器

        self.openAddWin = AddStudent()  # 添加窗口实例
        self.openDelWin = del_window()  # 删除窗口实例
        self.helpWin = HelpWindow()  # 帮助窗口实例
        self.openAddClass = AddClassTable()  # 添加班级表实例
        self.openDelClass = DelClassTable()  # 删除班级表实例

        self.slot_init()
        self.photoNum = 0  # 照片计数
        self.CAM_NUM = 0
        # self.promptWin=prompt()
        self.combobox_init()  # 初始化下拉列表
        self.pNum = 0  # 照片计数器
        self.photo_transmission = 0  # 图片传输变量
        self.frame_out = 0

        # 启动Facenet模块
        # self.face = face_recognition.face()

    # 槽初始化
    def slot_init(self):
        self.btn_openCamera.clicked.connect(self.opencamera)
        self.btn_takePhoto.clicked.connect(self.take_photo)
        self.timer_camera_test.timeout.connect(self.show_frame)
        self.btn_addNewFace.clicked.connect(self.open_add_win)
        self.btn_delFace.clicked.connect(self.open_del_win)
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_train.clicked.connect(self.train)
        self.btn_recogniton.clicked.connect(self.open_recognition_camera)
        self.actionHelp.triggered.connect(self.open_help)
        self.actionAddClass.triggered.connect(self.open_add_class)
        self.actionDelClass.triggered.connect(self.open_del_class)

    def open_help(self):
        self.helpWin.show()

    def open_del_class(self):
        self.openDelClass.show()

    def open_add_class(self):
        self.openAddClass.show()

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

    # 打开添加窗口
    def open_add_win(self):
        self.openAddWin.show()

    # 打开删除窗口
    def open_del_win(self):
        self.openDelWin.show()

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
            selectClass = self.comboBox_selectClass.currentText()
            selectid = self.comboBox_selectId.currentText()

            name = '{CLASS}_{id}'.format(CLASS=selectClass, id=selectid)
            name = '../src_img/{name}.jpg'.format(name=name)
            print(name)
            cv2.imwrite(name, self.photo_transmission)

    # 获取班级列表
    def combobox_init(self, proclass=None):
        self.comboBox_selectClass.clear()
        table_name, table_nmu = self.opsql.select_all_table()
        readlines = table_nmu
        lineindex = 0
        while lineindex < readlines:
            self.comboBox_selectClass.addItem(table_name[lineindex])
            lineindex += 1
        if proclass != '':
            self.comboBox_selectClass.setCurrentText(proclass)

    # 刷新显示
    def refresh(self):
        proclass = self.comboBox_selectClass.currentText()
        self.combobox_init(proclass=proclass)
        id = self.opsql.show_student_id(proclass)
        for i in range(len(id)):
            print(id[i])
            self.comboBox_selectId.addItem(str(id[i]))

    def train(self):
        msg = QtWidgets.QMessageBox.information(self, u"提示", u"训练过程中，画面无法更新。",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
        get_face.detection()

    # 打开识别摄像头
    def open_recognition_camera(self):
        msg = QtWidgets.QMessageBox.information(self, u"启动提示", u"1、启动时间根据设备性能强弱决定\n\n2、程序启动后按下esc退出检测窗口",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)

        if self.btn_openCamera.text() == '关闭摄像头':
            msg = QtWidgets.QMessageBox.warning(self, u"警告", u"请先关闭摄像头!",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            print('开启摄像头')
            self.face.main(False)
            # self.lab_frame.setText(u"正在加载并启动程序...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit((app.exec_()))
