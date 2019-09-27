import cv2
from main_ui import Ui_Face_Recognition_window
from addFace_ui import Ui_Form
from delwin_ui import Ui_Form_Del
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from file_op import File_Operate
from sqlite3_op import Operate_Sql
import sqlite3 as db
import os


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

        :return:
        '''
        text = self.line_delFaceName.text()
        flag = self.opsql.Select_Same_Name(text)
        if flag is False:  # 如果数据库不存在这个目录
            msg = QtWidgets.QMessageBox.warning(self, u"警告", u"不存在这个用户",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)

        else:
            # self.opfile.Delete_File(text)
            self.opsql.Delete_File_Name(text)
            msg = QtWidgets.QMessageBox.information(self, u"完成", u"删除完成！",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            self.line_delFaceName.clear()


# 添加窗口类
class add_window(QDialog, Ui_Form):
    def __init__(self):
        super(add_window, self).__init__()
        self.setupUi(self)
        self.slotInit()
        self.opsql = Operate_Sql()
        self.opfile = File_Operate()
        self.line_addFaceName.clear()

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
        3、从数据库读取名字列表
        '''
        text = self.line_addFaceName.text()  # 获取输入文本
        flag = self.opsql.Select_Same_Name(str(text))  # 查看数据库中是否存在相同的名字
        print(flag)
        if flag is True:
            msg = QtWidgets.QMessageBox.warning(self, u"警告", u"存在名字以存在，请更改",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            if len(text) == 0:  # 如果目录为空
                msg = QtWidgets.QMessageBox.warning(self, u"警告", u"目录为空",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                # 根据用户名构建插入语句
                newName = self.opsql.CreatSqlStr(text)
                self.opsql.Insert_New_Name(newName)  # 向数据库插入新行
                self.btn_hide()  # 隐藏窗口
                # ret = self.opfile.Create_File(text)  # 创建文件夹
                # if ret:
                #     msg = QtWidgets.QMessageBox.information(self, u"完成", u"个人文件夹创建成功！",
                #                                             buttons=QtWidgets.QMessageBox.Ok,
                #                                             defaultButton=QtWidgets.QMessageBox.Ok)
                #     self.line_addFaceName.clear()
                #     self.opsql.Select_All_Name()
                # else:
                #     msg = QtWidgets.QMessageBox.critical(self, u"失败", u"无法创建个人文件夹",
                #                                          buttons=QtWidgets.QMessageBox.Ok,
                #                                          defaultButton=QtWidgets.QMessageBox.Ok)


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
        self.timer_camera = QtCore.QTimer()  # qt计数器

        self.slot_init()

        self.photoNum = 0  # 照片计数
        self.CAM_NUM = 0

        self.openAddWin = add_window()  # 添加窗口实例
        self.openDelWin = del_window()  # 删除窗口实例

        self.Combobox_Init()  # 初始化下拉列表
        self.lab_faceNumShow.setText(str(self.opsql.Num_Now_All()) + '张')  # 显示数据库中存在的人脸个数
        self.lab_selecFile.setText("选择文件夹")
        self.pNum = 0;  # 照片计数器
        self.photo_transmission=0#图片传输变量

    # 槽初始化
    def slot_init(self):
        self.btn_openCamera.clicked.connect(self.OpenCamera)
        self.btn_takePhoto.clicked.connect(self.Take_Photo)
        self.timer_camera.timeout.connect(self.Show_Frame)

        self.btn_addFace.clicked.connect(self.open_Add_Win)
        self.comboBox_selectFile.currentIndexChanged.connect(self.Show_Select_Cbb)
        self.btn_delFace.clicked.connect(self.open_Del_Win)
        self.btn_refresh.clicked.connect(self.Refresh)

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
    def open_Add_Win(self):
        self.openAddWin.show()

    # 打开删除窗口
    def open_Del_Win(self):
        self.openDelWin.show()

    # 拍照
    def Take_Photo(self):
        '''
        1、从数据库中读取所有文件名
        2、从文件名中选择文件目录作为照片存储地址
        3、调用拍照程序对当前画面进行拍照
        4、更新拍照数量
        '''

        selectFName=self.comboBox_selectFile.currentText()
        fName='../faces/'+selectFName+'/photo_%s.jpg'%self.pNum
        fPaht = '../faces/' + selectFName
        # print(os.path.isdir(fName))
        if self.btn_openCamera.text()!='关闭摄像头':
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请打开摄像头!",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            if os.path.isdir(fPaht) is False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"不存在这个目录!",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.pNum += 1
                self.lab_faceNumDisplay.setText('%d' %self.pNum)
                # print(selectFName)
                # print(fName)
                # print(self.pNum)
                cv2.imwrite(fName,self.photo_transmission)

    # 获取文件夹名字列表
    def Combobox_Init(self):
        '''
        1、根据sql语句从数据库中读取所有文件名
        '''
        self.comboBox_selectFile.clear()
        num = self.opsql.Num_Now_All()
        rows = self.opsql.readFronSqllite(self.DB_Path, self.sqlStr_SelectAll)
        readLines = num
        lineIndex = 0
        while lineIndex < readLines:
            row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
            self.comboBox_selectFile.addItem(str(row[0]))
            lineIndex += 1

    def Show_Select_Cbb(self):
        self.lab_selecFile.setText('选择了：' + self.comboBox_selectFile.currentText())

    # 训练模型
    def Train(self):
        '''
        1、调用训练文件进行整体训练
        2、更新进度条和提示字符串
        '''
        pass

    # 刷新显示
    def Refresh(self):
        self.Combobox_Init()
        self.lab_faceNumShow.setText(str(self.opsql.Num_Now_All()) + '张')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit((app.exec_()))
