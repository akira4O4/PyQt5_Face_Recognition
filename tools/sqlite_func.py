import sqlite3 as db

test_db_path = "/home/lee/pyCode/PyQt5_Face_Recognition/DB/StudentFaceDB.db"


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
        conn.commit()
        conn.close()
        return rows

    # 返回当前当前数据库所有表
    def check_table(self, db_path):
        self._table = "select name from sqlite_master where type='table' order by name"
        ret = self.executeCMD(db_path, self._table)
        self.table_list = []
        for i in ret:
            self.table_list.append(i[0])
        return self.table_list

    # 查看表结构
    def check_field(self, db_path, t):
        self.field_list = []
        self._schema = lambda t: "PRAGMA table_info({})".format(t)
        ret = self.executeCMD(db_path, self._schema(t))
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
    def update(self, db_path, table, field, data, primary_key_index):
        print("upate new date...")
        for i in range(len(data)):
            # 删除修改的数据项
            # DELETE FROM table_name WHERE [condition];
            cmd = "delete from {} where {}='{}';".format(str(table), field[primary_key_index],
                                                         data[i][primary_key_index])
            print("execute cmd={}".format(cmd))
            ret = self.executeCMD(db_path, cmd)
            print("ret=", ret)
        for i in range(len(data)):
            # 插入新数据
            # INSERT INTO TABLE_NAME VALUES (value1,value2,value3,...valueN);
            cmd = ', '.join(list(map(lambda x: "'" + x + "'", data[i])))
            cmd = "INSERT INTO {} VALUES ({});".format(table, cmd)
            print("execute cmd={}\n".format(cmd))
            ret = self.executeCMD(db_path, cmd)
            print("ret:", ret)
        return 0

    # 查找一个表中的主键位置
    # para:db路径，表名
    # return primary_key_index,primary_key
    def find_primary_key(self, db_path, table):
        cmd = "pragma table_info ({});".format(str(table))
        ret = self.executeCMD(db_path, cmd)
        print(ret)
        num = len(ret[0]) - 1
        for i in range(len(ret)):
            if ret[i][num] == 1:
                print("{}:{}是主键".format(i, ret[i][1]))
                return i, ret[i][1]

    # 删除
    # param:表，主键，参数
    def delete(self, db_path, table_name, primary_key, primary_key_index, data):
        # DELETE FROM table_name WHERE [condition];
        cmd = "DELETE FROM {} WHERE {}='{}';".format(table_name, primary_key, data[primary_key_index])
        print("del cmd:", cmd)
        self.executeCMD(db_path,cmd)

    def insert(self,db_path,table,data):
        pass


if __name__ == "__main__":
    t = Sqlite_Func()
    # t.find_primary_key(test_db_path,"CS172")
    field = ['lable', 'name', 'sex', 'id', 'profession', 'features', 'flag']
    print(field[3])
    t.update("CS172", field, [], 3)
'''
CREATE TABLE table_test(
    lable   text not null,
    name    text not null,
    sex     text not null,
    id      text primary key not null,
    profession text not null,
    featrues text not null
);
'''
