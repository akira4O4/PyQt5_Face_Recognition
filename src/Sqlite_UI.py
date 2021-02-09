import sys

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication

from ui_src.sqlite_main_window import Ui_SqliteMainWindow

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

    def open_db(self):
        print("打开文件")
        self.file_path, file_type = QFileDialog.getOpenFileName(self, "select db files", "",
                                                                "*.db;;*.png;;All Files(*)")
        print("文件路径:{}\n文件类型:{}\n".format(self.file_path, file_type))

        self.table_list = self.sf.check_table(self.file_path)
        print("当前数据库含有表：", self.table_list)

        ret = self.sf.check_field(self.file_path, self.table_list[0])
        print("当前{}表字段{}".format(self.table_list[0], ret))

        # 设置窗口名字
        QDialog.setWindowTitle(self, self.file_path)

        self.create_radiobox_table()

    def create_radiobox_table(self):
        self.btn_list=[]
        self.vboxlayer = QVBoxLayout()

        for data in self.table_list:
            self.btn_list.append(QtWidgets.QRadioButton("{}".format(data)))

        for btn in self.btn_list:
            self.vboxlayer.addWidget(btn)

        self.groupBox_table.setLayout(self.vboxlayer)

    def create_checkbox_field(self):
        pass

    def query(self):
        pass

    def add(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Sqlite_UI()
    ui.show()
    sys.exit((app.exec_()))
