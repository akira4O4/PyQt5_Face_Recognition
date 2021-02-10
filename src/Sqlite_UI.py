import sys

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.Qt import Qt
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

        self.file_path = ""

        # 表列表
        self.table_list = []
        # 表字段列表
        self.field_list = []

    def slot_init(self):
        print("slot init...")
        self.actionOpen_File.triggered.connect(self.open_db)
        self.radioButton_all.clicked.connect(self.selectAll_radiobtn)
        self.radioButton_notall.clicked.connect(self.selectNotAll_radiobtn)

    def open_db(self):
        print("打开文件")
        self.file_path, file_type = QFileDialog.getOpenFileName(self, "select db files", "",
                                                                "*.db;;*.png;;All Files(*)")
        print("文件路径:{}\n文件类型:{}\n".format(self.file_path, file_type))

        self.table_list = self.sf.check_table(self.file_path)
        print("当前数据库含有表：", self.table_list)

        # 设置窗口名字
        QDialog.setWindowTitle(self, self.file_path)

        self.create_radiobox_table()

    # 创建单选表项
    def create_radiobox_table(self):
        self.count = 0
        self.btn_layer = QWidget()
        for i, data in enumerate(self.table_list):
            self.count += 1
            self.btn = QtWidgets.QRadioButton(self.btn_layer)
            self.btn.setText(str(data))
            self.table=self.btn.text()
            self.btn.clicked.connect(partial(self.create_checkbox_field, self.table, False))
            self.btn.move(10, i * 60)

        self.btn_layer.setMinimumSize(250, self.count * 60)
        self.scrollArea_table.setWidget(self.btn_layer)
        self.scrollArea_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # 创建多选字段项
    def create_checkbox_field(self, table, ischeck):
        print("选择了{}表".format(str(table)))
        ret = self.sf.check_field(self.file_path, table)
        print("当前表含有{}字段:".format(ret))
        self.field_list = []
        self.count = 0
        self.btn_layer = QWidget()
        for i, data in enumerate(ret):
            self.count += 1
            self.btn = QtWidgets.QCheckBox(self.btn_layer)
            self.btn.setText(str(data))
            self.btn.setChecked(ischeck)
            self.btn.move(10, i * 60)
            self.field_list.append(self.btn)

        self.btn_layer.setMinimumSize(250, self.count * 60)
        self.scrollArea_field.setWidget(self.btn_layer)
        self.scrollArea_field.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def selectAll_radiobtn(self):
        if self.field_list == []:
            print("没有选择表")
        else:
            print("全选字段")
            self.create_checkbox_field(self.table,True)

    def selectNotAll_radiobtn(self):
        if self.field_list == []:
            print("没有选择表")
        else:
            print("全选字段")
            self.create_checkbox_field(self.table, False)

    def show_table(self):
        print("显示表内容")

    def query(self):
        pass

    def add(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Sqlite_UI()
    ui.show()
    sys.exit((app.exec_()))
