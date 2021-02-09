import sys

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication

from ui_src.sqlite_main_window import Ui_SqliteMainWindow


class Sqlite_UI(QtWidgets.QMainWindow, Ui_SqliteMainWindow):
    def __init__(self, parent=None):
        super(Sqlite_UI, self).__init__(parent)
        self.setupUi(self)
        self.slot_init()

    def slot_init(self):
        print("slot init...")
        self.actionOpen_File.triggered.connect(self.open_db)

    def open_db(self):
        print("打开文件")
        file_name, file_type = QFileDialog.getOpenFileName(self, "select db files", "", "*.db;;*.png;;All Files(*)")
        print("文件路径:{}\n文件类型:{}\n".format(file_name, file_type))

    def query(self):
        pass

    def add(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Sqlite_UI()
    ui.show()
    sys.exit((app.exec_()))
