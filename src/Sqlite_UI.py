import sys

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QAbstractItemView
from PyQt5.Qt import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui_src.sqlite_main_window import Ui_SqliteMainWindow
from functools import partial

from tools.sqlite_func import Sqlite_Func


class Sqlite_UI(QtWidgets.QMainWindow, Ui_SqliteMainWindow):
    def __init__(self, parent=None):
        super(Sqlite_UI, self).__init__(parent)
        self.setupUi(self)

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

    def slot_init(self):
        print("slot init...")
        self.actionOpen_File.triggered.connect(self.open_db)
        self.radioButton_all.clicked.connect(self.selectAll_radiobtn)
        self.radioButton_notall.clicked.connect(self.selectNotAll_radiobtn)
        # 查询
        self.pushButton_query.clicked.connect(self.query)
        self.pushButton_update.clicked.connect(self.update_data)
        self.pushButton_del.clicked.connect(self.delete)
        self.pushButton_add.clicked.connect(self.add)
    def open_db(self):
        print("打开文件")
        self.db_path, file_type = QFileDialog.getOpenFileName(self, "select db files", "",
                                                              "*.db;;*.png;;All Files(*)")
        print("文件路径:{}\n文件类型:{}\n".format(self.db_path, file_type))

        self.table_list = self.sf.check_table(self.db_path)
        print("当前数据库含有表：", self.table_list)

        # 设置窗口名字
        QDialog.setWindowTitle(self, self.db_path)

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
        # self.field_list.clear()
        # self.select_field_list.clear()
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
            self.btn.setText(str(data))
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
        self.model = QStandardItemModel(self.len_row, self.len_col, self)
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
            for i in range(self.len_row):
                print("i: ", i)
                update_data_item = []
                for j in range(self.len_col):
                    update_data_item.append(self.model.item(i, j).text())
                update_data.append(update_data_item)
            print("update data", update_data)
            i, key = self.sf.find_primary_key(self.db_path, self.table)
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

        print("self.select_field_list:",self.select_field_list)
        if self.select_field_list != []:
            str_sql = self.sf.auto_select(self.select_field_list, self.table)
            print("str sql:{}".format(str_sql))
            ret = self.sf.executeCMD(self.db_path, str_sql)
            print(ret)
            for i, data in enumerate(ret):
                print("{}->{}\n".format(i, data))
            self.show_table(self.select_field_list, ret)
        if self.select_field_list==[]:
            self.tableView_content.setModel(self.model.clear())

    # 进行删除操作需要选中所有字段
    def delete(self):
        # if self.tableView_content.currentIndex().row() != "" and self.table != "" and self.model!=None:
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
            for i in range(len(self.field_list)):
                if self.model.item(del_row, i).text() != None:
                    del_data.append(self.model.item(del_row, i).text())
                    if len(del_row) != len(self.field_list):
                        print("数据不全")
                    else:
                        print("del data:", del_data)
                    self.sf.delete(self.db_path, self.table, key, key_idx, del_data)
                    self.query()

    def add(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Sqlite_UI()
    ui.show()
    sys.exit((app.exec_()))
