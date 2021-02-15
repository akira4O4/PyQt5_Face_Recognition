import sys

from PyQt5.QtWidgets import QDialog, QLabel, QTableView, QLineEdit, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QAbstractItemView
from PyQt5.Qt import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal

from ui_src.sqlite_main_window import Ui_SqliteMainWindow
from ui_src.Add_Data import Ui_Dialog_Add_Data
from ui_src.Add_Table import Ui_Dialog_Add_Table
from functools import partial
from tools.sqlite_func import Sqlite_Func


class Add_Table_UI(QDialog, Ui_Dialog_Add_Table):
    signal_status = pyqtSignal()

    def __init__(self, db_path, parent=None):
        super(Add_Table_UI, self).__init__(parent)

        self.db_path = db_path

        self.sf = Sqlite_Func()

        h_layout = QHBoxLayout()
        label_table_name = QLabel("表名字:")
        self.lineEdit_table_name = QLineEdit()
        # 水平放置
        h_layout.addWidget(label_table_name)
        h_layout.addWidget(self.lineEdit_table_name)

        btn_ok = QPushButton()
        btn_ok.setText("OK")

        v_layout = QVBoxLayout()

        # 垂直放置
        v_layout.addLayout(h_layout)
        v_layout.addWidget(btn_ok)

        self.setLayout(v_layout)

        btn_ok.clicked.connect(self.create_table)

    def create_table(self):
        sstr = self.db_path.split('/')
        self.db_type = sstr[len(sstr) - 1]
        print("db_type:",self.db_type)
        print("创建新表")
        if self.lineEdit_table_name == "":
            print("表名字为空")
        else:
            self.sf.create_table(self.db_path, self.lineEdit_table_name.text(), str(self.db_type).upper())
            status = 1

            self.signal_status.emit()
            self.close()

    def test(self, s):
        print("s:", s)


class Add_Data_UI(QDialog, Ui_Dialog_Add_Data):
    signal_status = pyqtSignal()

    def __init__(self, db_path, table, field, parent=None):
        super(Add_Data_UI, self).__init__(parent)

        self.db_path = db_path
        self.table = table
        self.field = field

        self.sf = Sqlite_Func()

        v_label_layout = QVBoxLayout()
        v_lineEdit_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout()
        self.lineEdit_list = []
        self.field_len = len(field)
        for i in range(self.field_len):
            label = QLabel()
            label.setText("{}:".format(str(field[i]).upper()))
            v_label_layout.addWidget(label)

            lineEdit = QLineEdit()
            self.lineEdit_list.append(lineEdit)
            v_lineEdit_layout.addWidget(lineEdit)

        h_layout.addLayout(v_label_layout)
        h_layout.addLayout(v_lineEdit_layout)

        btn_ok = QPushButton()
        btn_ok.setText("确定")

        v_layout.addLayout(h_layout)
        v_layout.addWidget(btn_ok)

        self.setLayout(v_layout)

        self.setupUi(self)
        btn_ok.clicked.connect(self.insert_data)

    def insert_data(self):
        lineEdit_data = []
        for i in range(len(self.lineEdit_list)):
            lineEdit_data.append(self.lineEdit_list[i].text())

        # 插入数据库
        self.sf.insert(self.db_path, self.table, lineEdit_data)
        self.signal_status.emit()
        self.close()


class Sqlite_UI(QtWidgets.QMainWindow, Ui_SqliteMainWindow):
    def __init__(self, parent=None):
        super(Sqlite_UI, self).__init__(parent)
        self.setupUi(self)

        # 隐藏两个组件：因为我不想写了
        self.label_cmd.hide()
        self.lineEdit_cmd.hide()

        # slot init
        self.slot_init()

        self.sf = Sqlite_Func()

        # 数据库路径
        self.db_path = ""
        # 选择的表名
        self.table = ""
        # 所有数据表
        self.table_list = []
        # 当前表所有字段
        self.field_list = []
        # 创建的按钮字段列表
        self.btn_field_list = []
        # 被勾选的字段
        self.select_field_list = []
        #当前行列
        self.len_row = 0
        self.len_col = 0

        self.model = QStandardItemModel()

        #数据库类型
        self.db_type=""

    def slot_init(self):
        print("slot init...")
        self.actionOpen_File.triggered.connect(self.open_db)

        self.radioButton_all.clicked.connect(self.selectAll_radiobtn)
        self.radioButton_notall.clicked.connect(self.selectNotAll_radiobtn)

        self.pushButton_query.clicked.connect(self.query)
        self.pushButton_update.clicked.connect(self.update_data)
        self.pushButton_del.clicked.connect(self.delete_data)
        self.pushButton_add.clicked.connect(self.add_data)
        self.pushButton_delTable.clicked.connect(self.del_table)
        self.pushButton_newTable.clicked.connect(self.add_table)

    def open_db(self):
        print("打开文件")
        self.db_path, file_type = QFileDialog.getOpenFileName(self, "select db files", "",
                                                              "*.db;;*.png;;All Files(*)")
        print("文件路径:{}\n文件类型:{}\n".format(self.db_path, file_type))

        self.table_list = self.sf.check_table(self.db_path)
        print("当前数据库含有表：", self.table_list)

        # 设置窗口名字
        QDialog.setWindowTitle(self, self.db_path)
        sstr = self.db_path.split('/')

        print(sstr)
        self.groupBox_table_field.setTitle("数据库：{}".format(sstr[len(sstr) - 1]))

        self.db_type=sstr[len(sstr) - 1]

        self.create_radiobox_table()

    # 创建数据库表选项
    def create_radiobox_table(self):
        self.count = 0
        self.btn_layer = QWidget()
        for i, data in enumerate(self.table_list):
            self.count += 1
            self.btn = QtWidgets.QRadioButton(self.btn_layer)
            self.btn.setText(str(data))
            self.btn.clicked.connect(partial(self.create_checkbox_field, self.btn.text(), False))
            self.btn.move(10, i * 60)

        self.btn_layer.setMinimumSize(250, self.count * 60)
        self.scrollArea_table.setWidget(self.btn_layer)
        self.scrollArea_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # 创建字段表
    def create_checkbox_field(self, table, ischeck):
        self.btn_field_list.clear()
        self.count = 0

        self.table = table
        print("选择了{}表".format(str(table)))
        ret = self.sf.check_field(self.db_path, table)
        self.field_list = ret
        print("当前表含有{}字段:".format(ret))
        self.btn_layer = QWidget()
        for i, data in enumerate(ret):
            self.count += 1
            self.btn = QtWidgets.QCheckBox(self.btn_layer)
            self.btn.setText("{}".format(str(data)))
            self.btn.setChecked(ischeck)
            self.btn.move(10, i * 60)
            self.btn_field_list.append(self.btn)

        self.btn_layer.setMinimumSize(250, self.count * 60)
        self.scrollArea_field.setWidget(self.btn_layer)
        self.scrollArea_field.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def selectAll_radiobtn(self):
        if self.btn_field_list == []:
            print("没有选择表")
        else:
            print("全选字段")
            self.create_checkbox_field(self.table, True)
            self.select_field_list.clear()
            for btn in self.btn_field_list:
                self.select_field_list.append(btn.text())

    def selectNotAll_radiobtn(self):
        if self.btn_field_list == []:
            print("没有选择表")
        else:
            print("全选字段")
            self.create_checkbox_field(self.table, False)
            self.select_field_list.clear()

    # param:字段，内容
    def show_table(self, fields, data):
        print("显示表内容")
        print("字段:{}\n数据:{}".format(fields, data))

        # 行数
        # 列数
        self.len_row = len(data)
        self.len_col = len(fields)
        print("row:{},col:{}".format(self.len_row, self.len_col))
        # self.model = QStandardItemModel(self.len_row, self.len_col, self)
        self.model.setRowCount(self.len_row)
        self.model.setColumnCount(self.len_col)
        for row in range(self.len_row):
            for col in range(len(data[0])):
                item = QStandardItem("{}".format(data[row][col]))
                self.model.setItem(row, col, item)

        self.tableView_content.setModel(self.model)
        self.tableView_content.horizontalHeader().setStretchLastSection(True)
        self.tableView_content.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.tableView_content.clicked.connect(lambda x: print(self.tableView_content.currentIndex().data()))

    # 通过按键更新数据到数据库
    def update_data(self):
        print(self.btn_field_list)
        if self.btn_field_list == []:
            print("没有选择表")
        else:
            update_data = []
            if self.len_row == 0:
                print("没有数据")
                return

            # 读取新数据
            for i in range(self.len_row):
                update_data_item = []
                for j in range(self.len_col):
                    if self.model.item(i, j).text() != None:
                        update_data_item.append(self.model.item(i, j).text())
                update_data.append(update_data_item)
            print("update data", update_data)

            if len(update_data[0]) != len(self.field_list):
                print("数据不足")
                return
            # 查找主键
            i, key = self.sf.find_primary_key(self.db_path, self.table)
            # 更新数据
            ret = self.sf.update(self.db_path, self.table, self.field_list, update_data, i)
            if ret != 0:
                print("更新失败\n")
            else:
                print("更新完成\n")

    # 查询
    def query(self):
        self.select_field_list.clear()
        for btn in self.btn_field_list:
            print(btn.isChecked())
            if btn.isChecked() == True:
                self.select_field_list.append(btn.text())

        print("self.select_field_list:", self.select_field_list)

        if self.select_field_list != []:

            # 根据所选字段和表构建查询语句：select field1,field2,...,fieldN from table
            str_sql = self.sf.auto_select(self.select_field_list, self.table)
            ret = self.sf.executeCMD(self.db_path, str_sql)
            print(ret)
            for i, data in enumerate(ret):
                print("{}->{}\n".format(i, data))

            # 打印数据
            self.show_table(self.select_field_list, ret)

        if self.select_field_list == []:
            self.tableView_content.setModel(self.model.clear())

    # 进行删除操作需要选中所有字段
    def delete_data(self):
        if self.table == "":
            print("未选择表")
            return
        if self.select_field_list == []:
            print("未选择字段")
            return
        if self.tableView_content.currentIndex().row() == -1:
            print("未选择数据")
            return
        else:
            del_row = self.tableView_content.currentIndex().row()
            print("选择{}行".format(del_row))

            # 主键index和获取主键
            key_idx, key = self.sf.find_primary_key(self.db_path, self.table)
            del_data = []
            # 读取当前行所有数据
            for i in range(self.len_col):
                if self.model.item(del_row, i).text() != None:
                    del_data.append(self.model.item(del_row, i).text())

            if len(del_data) != len(self.field_list):
                print("数据不全")
                return
            print("del data:", del_data)
            self.sf.delete(self.db_path, self.table, key, key_idx, del_data)
            self.query()

    def add_data(self):
        if self.db_path == "":
            print("未选择数据库")
            return
        if self.table == "":
            print("未选择表")
            return
        if self.select_field_list == []:
            print("未选择字段")
            return

        print("添加数据")
        self.add_data_ui = Add_Data_UI(self.db_path, self.table, self.field_list)
        self.add_data_ui.show()
        self.add_data_ui.signal_status.connect(self.query)
        # self.query()

    def flash_table(self):
        # 刷新数据库表
        self.table_list = self.sf.check_table(self.db_path)
        print("当前数据库含有表：", self.table_list)
        self.create_radiobox_table()

    def add_table(self):

        if self.db_path == "":
            print("没有选择数据库")
        else:
            self.add_table_ui = Add_Table_UI(self.db_path)
            self.add_table_ui.show()

            # 子窗口链接主窗口函数
            self.add_table_ui.signal_status.connect(self.flash_table)

    def del_table(self):
        if self.table == "":
            print("没有选择表")
            return
        print("当前选择表:{}".format(self.table))
        self.sf.delete_table(self.db_path, self.table)
        self.tableView_content.setModel(self.model.clear())

        # 刷新数据库表
        self.table_list = self.sf.check_table(self.db_path)
        print("当前数据库含有表：", self.table_list)
        self.create_radiobox_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Sqlite_UI()
    # ui = Add_Data_UI()
    ui.show()
    sys.exit((app.exec_()))
