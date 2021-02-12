import sqlite3 as db

test_file_path = "/home/lee/pyCode/PyQt5_Face_Recognition/DB/StudentFaceDB.db"


class Sqlite_Func:
    def __init__(self):
        pass

    # 执行语句
    def executeCMD(self, db_path, exectCmd):
        if exectCmd == "":
            assert "func executeCMD error"
        conn = db.connect(db_path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
        if conn == None:
            return None
        cursor = conn.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
        conn.row_factory = db.Row  # 可访问列信息
        cursor.execute(exectCmd)  # 该例程执行一个 SQL 语句
        rows = cursor.fetchall()  # 该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。
        conn.close()
        return rows

    # 返回当前当前数据库所有表
    def check_table(self, file_path):
        self._table = "select name from sqlite_master where type='table' order by name"
        ret = self.executeCMD(file_path, self._table)
        self.table_list = []
        for i in ret:
            self.table_list.append(i[0])
        return self.table_list

    # 查看表结构
    def check_field(self, file_path, t):
        self.field_list = []
        self._schema = lambda t: "PRAGMA table_info({})".format(t)
        ret = self.executeCMD(file_path, self._schema(t))
        for i in ret:
            self.field_list.append(i[1])
        return self.field_list

    # 构建普通查询语句
    def auto_select(self, fields, table):
        str = ', '.join(list(map(lambda x: x, fields)))
        str = "select {} from {};".format(str, table)
        print(str)
        return str

    # 查询
    def query(self, db_path):
        if db_path == None or db_path == "":
            print("没有文件")
            return None

    # 更新
    def update(self,data,primary_key):
        return 0

    # 查找一个表中的主键位置
    # para:db路径，表名
    def find_primary_key(self, file_path, table):
        cmd = "pragma table_info ({});".format(str(table))
        ret = self.executeCMD(file_path, cmd)
        print(ret)
        print(len(ret))
        print(len(ret[0]))
        num = len(ret[0]) - 1
        for i in range(len(ret)):
            if ret[i][num] == 1:
                print("{}是主键".format(ret[i][1]))
                return ret[i][1]

    # 删除
    def delete(self, db_path):
        pass


if __name__ == "__main__":
    s = Sqlite_Func()
    s.find_primary_key(test_file_path, "CS172")

    l1=[1,2,3]
    l2=[4,5,6]
    l3=[]
    l3.append(l1)
    print(l3)
    l1.clear()
    l1=[5,5,5]
    l3.append(l1)
    print(l3)
