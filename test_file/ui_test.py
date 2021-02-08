import sys

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication

from src.sqlite3_main import Ui_sqlite3_mainWindow


class Sqlite_UI_Test(QDialog, Ui_sqlite3_mainWindow):
	def __init__(self, parent=None):
		super(Sqlite_UI_Test, self).__init__(parent)
		self.setupUi(self)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = Sqlite_UI_Test()
	ui.show()
	sys.exit((app.exec_()))
