import cv2
import sys
import time
import os

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

import get_face
import face_recognition
from file_op import File_Operate
from sqlite3_op import Operate_Sql
from tools.sqlite_func import Sqlite_Func

from ui_src.MainUI import Ui_Face_Recognition_window
from ui_src.addStudent import Ui_Form_Student
from ui_src.delwin_ui import Ui_Form_Del

from ui_src.addClassTable import Ui_AddClassTable
from ui_src.deleteClassTable import Ui_DelClassTable
from ui_src.help import Ui_help
from ui_src.checkTable import Ui_Form_checkTable
from ui_src.delCheckTable import Ui_Form_delCheckTable

from Sqlite_UI import Sqlite_UI


# class del_window(QDialog, Ui_Form_Del):
#     def __init__(self):
#         super(del_window, self).__init__()
#         self.setupUi(self)
#         self.SlotInit()
#         self.opsql = Operate_Sql()
#         self.opfile = File_Operate()
#         self.combobox_face_init()
#
#     def SlotInit(self):
#         self.btn_Cancel.clicked.connect(self.btn_hide)
#         self.btn_Enter.clicked.connect(self.btn_enter)
#         self.btn_Refresh.clicked.connect(self.refresh)
#
#     def btn_hide(self):
#         self.hide()
#
#     def refresh(self):
#         checked_table = self.comboBox_face.currentText()
#         self.combobox_face_init(checked_table=checked_table)
#         id = self.opsql.show_student_id(checked_table)
#         self.comboBox_id.clear()
#         for i in range(len(id)):
#             print(id[i])
#             self.comboBox_id.addItem(str(id[i]))
#
#     # 获取班级列表
#     def combobox_face_init(self, checked_table=None):
#         self.comboBox_face.clear()
#         table_name, table_nmu = self.opsql.select_all_table()
#         readlines = table_nmu
#         lineindex = 0
#         while lineindex < readlines:
#             self.comboBox_face.addItem(table_name[lineindex])
#             lineindex += 1
#         if checked_table != '':
#             self.comboBox_face.setCurrentText(checked_table)
#
#     def btn_enter(self):
#         CLASS = self.comboBox_face.currentText()
#         id = self.comboBox_id.currentText()
#
#         # 从本地删除src_img文件
#         path_src = '../src_img/{CLASS}_{id}.jpg'.format(CLASS=CLASS, id=id)
#         path_emb = '../emb_img/{CLASS}_{id}.jpg'.format(CLASS=CLASS, id=id)
#
#         if os.path.exists(path_src):
#             os.remove(path_src)
#         # 从本地删除emb_img文件
#         if os.path.exists(path_emb):
#             os.remove(path_emb)
#
#         self.opsql.Delete_File_Name(CLASS, id)  # 从数据库中删除这个文件名
#         msg = QtWidgets.QMessageBox.information(self, u"完成", u"删除完成！",
#                                                 buttons=QtWidgets.QMessageBox.Ok,
#                                                 defaultButton=QtWidgets.QMessageBox.Ok)
#
#         self.combobox_face_init()


# 删除考勤表
# class DelCheckTable(QDialog, Ui_Form_delCheckTable):
#     def __init__(self):
#         super(DelCheckTable, self).__init__()
#         self.setupUi(self)
#         self.initslot()
#         self.opsql = Operate_Sql()
#         self.opfile = File_Operate()
#         self.comboBox_delCheckTable.clear()
#         self.init_check_table()
#
#     def init_check_table(self):
#         table_name, table_nmu = self.opsql.select_all_checktable()
#         readlines = table_nmu
#         lineindex = 0
#         while lineindex < readlines:
#             row = table_name[lineindex]  #
#             self.comboBox_delCheckTable.addItem(table_name[lineindex])
#             lineindex += 1
#
#     def initslot(self):
#         self.btn_cancel.clicked.connect(self.btn_hide)
#         self.btn_confirm.clicked.connect(self.confirm)
#         self.btn_refresh.clicked.connect(self.refresh)
#
#     def refresh(self):
#         self.comboBox_delCheckTable.clear()
#         self.init_check_table()
#
#     def btn_hide(self):
#         self.hide()
#
#     def confirm(self):
#         check_name = self.comboBox_delCheckTable.currentText()
#         flag = self.opsql.delete_check_table(check_name)
#         if flag:
#             print("完成")
#             msg = QtWidgets.QMessageBox.information(self, u"完成", u"删除成功！",
#                                                     buttons=QtWidgets.QMessageBox.Ok,
#                                                     defaultButton=QtWidgets.QMessageBox.Ok)
#         else:
#             print('失败')
#             msg = QtWidgets.QMessageBox.warning(self, u"警告", u"不存在这个表，请更改",
#                                                 buttons=QtWidgets.QMessageBox.Ok,
#                                                 defaultButton=QtWidgets.QMessageBox.Ok)


# 删除人脸数据表
# class DelClassTable(QDialog, Ui_DelClassTable):
#     def __init__(self):
#         super(DelClassTable, self).__init__()
#         self.setupUi(self)
#         self.initslot()
#         self.opsql = Operate_Sql()
#         self.opfile = File_Operate()
#         self.init_facedate_table()
#         # 初始化信号槽
#
#     # 初始化
#     def init_facedate_table(self):
#         table_name, table_nmu = self.opsql.select_all_table()
#         readlines = table_nmu
#         lineindex = 0
#         while lineindex < readlines:
#             row = table_name[lineindex]  #
#             self.comboBox_del_facedata_table.addItem(table_name[lineindex])
#             lineindex += 1
#
#     def initslot(self):
#         self.btn_cancel.clicked.connect(self.btn_hide)
#         self.btn_confirm.clicked.connect(self.confirm)
#         self.btn_refresh.clicked.connect(self.refresh)
#
#     def refresh(self):
#         self.comboBox_del_facedata_table.clear()
#         self.init_facedate_table()
#
#     def btn_hide(self):
#         self.hide()
#
#     def confirm(self):
#         # 获取院系班级
#         facedate = self.comboBox_del_facedata_table.currentText()
#         flag = self.opsql.delete_pc_table(facedate)
#         if flag:
#             print("完成")
#             msg = QtWidgets.QMessageBox.information(self, u"完成", u"删除成功！",
#                                                     buttons=QtWidgets.QMessageBox.Ok,
#                                                     defaultButton=QtWidgets.QMessageBox.Ok)
#         else:
#             print('失败')
#             msg = QtWidgets.QMessageBox.warning(self, u"警告", u"不存在这个表，请更改",
#                                                 buttons=QtWidgets.QMessageBox.Ok,
#                                                 defaultButton=QtWidgets.QMessageBox.Ok)


# 添加考勤表
# class AddCheckTable(QDialog, Ui_Form_checkTable):
#     def __init__(self):
#         super(AddCheckTable, self).__init__()
#         self.setupUi(self)
#         self.initslot()
#         self.opsql = Operate_Sql()
#         self.opfile = File_Operate()
#         self.line_addCheckTable.clear()
#
#     # 初始化信号槽
#     def initslot(self):
#         self.btn_cancel.clicked.connect(self.btn_hide)
#         self.btn_confirm.clicked.connect(self.confirm)
#
#     def btn_hide(self):
#         self.hide()
#
#     def confirm(self):
#         check_table_name = self.line_addCheckTable.text()
#         flag = self.opsql.add_check_table(check_table_name)
#         if flag:
#             print("完成")
#             msg = QtWidgets.QMessageBox.information(self, u"完成", u"创建成功！",
#                                                     buttons=QtWidgets.QMessageBox.Ok,
#                                                     defaultButton=QtWidgets.QMessageBox.Ok)
#             time.sleep(0.3)
#             self.hide()
#
#         else:
#             print('失败')
#             msg = QtWidgets.QMessageBox.warning(self, u"警告", u"存在相同表名，请更改",
#                                                 buttons=QtWidgets.QMessageBox.Ok,
#                                                 defaultButton=QtWidgets.QMessageBox.Ok)


# 添加人脸数据表
# class AddClassTable(QDialog, Ui_AddClassTable):
#     def __init__(self):
#         super(AddClassTable, self).__init__()
#         self.setupUi(self)
#         self.initslot()
#         self.opsql = Operate_Sql()
#         self.opfile = File_Operate()
#         self.line_profession.clear()
#         self.line_class.clear()
#
#     # 初始化信号槽
#     def initslot(self):
#         self.btn_cancel.clicked.connect(self.btn_hide)
#         self.btn_confirm.clicked.connect(self.confirm)
#
#     def btn_hide(self):
#         self.hide()
#
#     def confirm(self):
#         # 获取院系班级
#         profession = self.line_profession.text()
#         class_ = self.line_class.text()
#         flag = self.opsql.create_new_pc_table(profession, class_)
#         self.line_profession.clear()
#         self.line_class.clear()
#         if flag:
#             print("完成")
#             msg = QtWidgets.QMessageBox.information(self, u"完成", u"创建成功！",
#                                                     buttons=QtWidgets.QMessageBox.Ok,
#                                                     defaultButton=QtWidgets.QMessageBox.Ok)
#             time.sleep(0.3)
#             self.hide()
#
#         else:
#             print('失败')
#             msg = QtWidgets.QMessageBox.warning(self, u"警告", u"存在相同表名，请更改",
#                                                 buttons=QtWidgets.QMessageBox.Ok,
#                                                 defaultButton=QtWidgets.QMessageBox.Ok)


# 添加新用户
# class AddStudent(QDialog, Ui_Form_Student):
#     def __init__(self):
#         super(AddStudent, self).__init__()
#         self.setupUi(self)
#         self.slotInit()
#         self.opsql = Operate_Sql()
#         self.opfile = File_Operate()
#         self.combobox_face_init()
#
#     def slotInit(self):
#         self.btn_cancel.clicked.connect(self.btn_hide)
#         self.btn_confirm.clicked.connect(self.btn_add_new_student)
#         self.btn_refresh.clicked.connect(self.refresh)
#         # 隐藏窗口
#
#     def btn_hide(self):
#         self.hide()
#
#     def refresh(self):
#         self.SelectClass.clear()
#         self.combobox_face_init()
#
#     # 初始化班级列表
#     def combobox_face_init(self):
#         table_name, table_nmu = self.opsql.select_all_table()
#         readlines = table_nmu
#         lineindex = 0
#         while lineindex < readlines:
#             self.SelectClass.addItem(table_name[lineindex])
#             lineindex += 1
#
#     def btn_add_new_student(self):
#         student_info = []
#         checked_table = self.SelectClass.currentText()
#         lable = self.line_addLabel.text()
#         name = self.line_addName.text()
#         sex = self.line_addSex.text()
#         id = self.line_addId.text()
#
#         student_info.append(lable)
#         student_info.append(name)
#         student_info.append(sex)
#         student_info.append(id)
#         student_info.append(checked_table)
#
#         # 检查学号是否唯一存在
#         flag = self.opsql.insert_new_student(student_info)
#         if flag:
#             msg = QtWidgets.QMessageBox.information(self, u"完成", u"添加个人信息完成！",
#                                                     buttons=QtWidgets.QMessageBox.Ok,
#                                                     defaultButton=QtWidgets.QMessageBox.Ok)
#             self.line_addLabel.clear()
#             self.line_addName.clear()
#             self.line_addSex.clear()
#             self.line_addId.clear()
#         else:
#             msg = QtWidgets.QMessageBox.warning(self, u"警告", u"存在相学号，请更改",
#                                                 buttons=QtWidgets.QMessageBox.Ok,
#                                                 defaultButton=QtWidgets.QMessageBox.Ok)


# # 提示窗口
# class HelpWindow(QDialog, Ui_help):
#     def __init__(self):
#         super(HelpWindow, self).__init__()
#         self.setupUi(self)


# 主窗口类
class MainWindow(QMainWindow, Ui_Face_Recognition_window):
    # 构造函数
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        # self.DB_Path = '../DB/FileNameDB.db'
        # self.sqlStr_SelectAll = "select * from fileName;"

        self.sf = Sqlite_Func()

        self.opsql = Operate_Sql()
        self.opfile = File_Operate()

        self.timer_camera_test = QtCore.QTimer()  # qt计数器
        self.timer_camera_face = QtCore.QTimer()  # qt计数器

        # self.openAddWin = AddStudent()  # 添加窗口实例
        # self.openDelWin = del_window()  # 删除窗口实例

        # self.helpWin = HelpWindow()  # 帮助窗口实例
        # self.openAddClass = AddClassTable()  # 添加班级表实例
        # self.openDelClass = DelClassTable()  # 删除班级表实例
        # self.openAddCheck = AddCheckTable()  # 添加考勤表示例
        # self.openDelCheck = DelCheckTable()  # 添加删除考勤表示例

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

    # 槽初始化
    def slot_init(self):

        self.timer_camera_test.timeout.connect(self.show_frame)

        self.btn_openCamera.clicked.connect(self.opencamera)
        self.btn_takePhoto.clicked.connect(self.take_photo)

        # self.btn_addNewFace.clicked.connect(self.open_add_win)
        # self.btn_delFace.clicked.connect(self.open_del_win)
        self.btn_refresh.clicked.connect(self.refresh)

        self.btn_train.clicked.connect(self.train)
        self.btn_recogniton.clicked.connect(self.open_recognition_camera)
        self.btn_sqlite.clicked.connect(self.open_sqlite)

        # self.actionHelp.triggered.connect(self.open_help)
        # self.actionAddClass.triggered.connect(self.open_add_class)
        # self.actionDelClass.triggered.connect(self.open_del_class)
        # self.actionAddCheck.triggered.connect(self.open_add_check_table)
        # self.actionDelCheck.triggered.connect(self.open_del_check)

    def open_sqlite(self):
        self.openSqlite.show()

    # def open_del_check(self):
    # self.openDelCheck.show()

    # def open_help(self):
    #     self.helpWin.show()

    # def open_del_class(self):
    #     self.openDelClass.show()

    # def open_add_class(self):
    #     self.openAddClass.show()

    # def open_add_check_table(self):
    #     self.openAddCheck.show()

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
    # def open_add_win(self):
    #     self.openAddWin.show()
    #
    # # 打开删除窗口
    # def open_del_win(self):
    #     self.openDelWin.show()

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
            selectClass = self.comboBox_face.currentText()
            selectid = self.comboBox_id.currentText()
            if selectid == '' or selectid is None:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请选择学号!",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                name = '{CLASS}_{id}'.format(CLASS=selectClass, id=selectid)
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
        # 读取人脸数据库中所有id
        field = []
        field.append("id")
        cmd = self.sf.auto_select(field, table)
        ret = self.sf.executeCMD(self.sf.DB_STUDENTFACE_PATH, cmd)
        print("ret:", ret)

        self.comboBox_id.clear()
        print(len(ret))
        for i in range(len(ret)):
            self.comboBox_id.addItem(str(ret[i][0]))

    # 刷新显示数据库并且显示id号
    def refresh(self):

        #获取当前选中表明
        checked_face = self.comboBox_face.currentText()
        checked_cw = self.comboBox_checkWork.currentText()

        print("当前选中：{},{}".format(checked_face, checked_cw))

        self.combobox_face_init(checked_table=checked_face)
        self.combobox_checkWork_init(checktable=checked_cw)
        #
        # id_set = self.opsql.show_student_id(checked_table)
        # self.comboBox_id.clear()
        # print(len(id_set))
        # for i in range(len(id_set)):
        #     print(id_set[i])
        #     self.comboBox_id.addItem(str(id_set[i]))

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
            CLASS = self.comboBox_face.currentText()
            ct = self.comboBox_checkWork.currentText()
            self.face.main(CLASS, ct)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit((app.exec_()))
