import sqlite3 as db


class Sqlite_Slot:
    def __init__(self):
        pass

    # 查询
    def query(self, db_path):
        if db_path == None or db_path == "":
            print("没有文件")
            return None

    # 删除
    def delete(self, db_path):
        pass


if __name__ == "__main__":
    ss = Sqlite_Slot()
