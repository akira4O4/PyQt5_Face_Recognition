import sqlite3 as db
import numpy as np


class Operate_Sql():
    def __init__(self):
        self.DB_Path = '../DB/FileNameDB.db'
        self.sqlStr_SelectAll = "select * from fileName;"
        self.sqlStr_InsertNewName = "insert into fileName(fName) values ("
        self.sqlStr_count = " select count(*) from fileName;"

    def readFronSqllite(self, db_path, exectCmd):
        conn = db.connect(db_path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
        cursor = conn.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
        conn.row_factory = db.Row  # 可访问列信息
        cursor.execute(exectCmd)  # 该例程执行一个 SQL 语句
        rows = cursor.fetchall()  # 该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。
        conn.close()
        return rows

    # 构建sql插入语句
    def CreatSqlStr(self, fileName):
        str = self.sqlStr_InsertNewName + "'" + fileName + "');"
        return str

    # 查询所有信息
    def Select_All_Name(self):
        num = self.Num_Now_All()
        rows = self.readFronSqllite(self.DB_Path, self.sqlStr_SelectAll)
        readLines = num
        lineIndex = 0
        while lineIndex < readLines:
            row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
            print(row[0], row[1], row[2])
            lineIndex += 1

    # 查询第一条信息
    def SelcetFirst(self):
        rows = self.readFronSqllite(self.DB_Path, self.sqlStr_SelectAll)
        readLines = 1
        lineIndex = 0
        while lineIndex < readLines:
            row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
            print('第一条数据是：', row[0], row[1], row[2], '\n')
            lineIndex += 1

    # 返回所有行数
    def Num_Now_All(self):
        num_all = self.readFronSqllite(self.DB_Path, self.sqlStr_count)
        return (num_all[0][0])

    # 插入一条信息
    def Insert_New_Name(self, filename):
        conn = db.connect(self.DB_Path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
        conn.execute(filename);
        conn.commit()
        print("插入完成\n");
        conn.close()

    # 查询是否存在相同的文件名
    def Select_Same_Name(self, name):
        rows = self.readFronSqllite(self.DB_Path, 'select * from fileName where fName ="' + str(name) + '";')
        if len(rows) == 0 or rows is None:  # 如果不存在相同名字的文件夹返回假
            # print(rows)
            print("不存在")
            return False
        else:  # 存在相同名字的文件夹返回真
            # print(len(rows))
            print("存在")
            # row = rows[0]  # 获取某一行的数据,类型是tuple
            # print('数据是：', row[0], row[1], '\n')
            return True

    def Delete_File_Name(self, filename):
        conn = db.connect(self.DB_Path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
        filename = 'delete from fileName where fName="' + filename + '";'
        print(filename)
        conn.execute(filename)
        conn.commit()
        print("删除完成")
        conn.close()

    # 插入embadding
    def insert_emb(self, fname, emb):
        list_emb = []
        str_emb = ''
        for i in range(128):
            list_emb.append(str(emb[i]))  # 加入到list
            str_emb = str_emb + ' ' + list_emb[i]  # list转str

        sql_find = 'select * from fileName where fName="' + fname + '";'
        sql_update_emb = 'update fileName set flag=1, embadding= "' + str_emb + '" where fName="' + fname + '";'
        sql_insert_emb = 'insert into fileName(fName,falg,embadding) values ("' + fname + '",1,"' + str_emb + '");'
        conn = db.connect(self.DB_Path)
        rows = self.readFronSqllite(self.DB_Path, sql_find)  # 查询这个fname有没有embadding

        if len(rows) == 0 or rows is None:  # 如果不存在相同名字的文件夹返回假
            print("不存在")
            conn.execute(sql_insert_emb)
            conn.commit()
            print("插入完成\n");
            conn.close()
        else:
            print('存在')
            row = rows[0]
            print(row)
            # if len(row[1]) == 0: #or row[2] is None:  # 当前label没有embadding，直接插入embadding
            print('没有embadding')
            conn.execute(sql_update_emb)
            conn.commit()
            print("插入完成\n");
            conn.close()
            # else:  # 更新embadding
            #     print('有embadding')
            #     conn.execute(sql_update_emb)
            #     conn.commit()
            #     print("更新完成\n");
            #     conn.close()

    def get_sql_emb(self):
        list_emb = []
        emb_temp = np.zeros(128)
        num = self.Num_Now_All()
        emb_arr = np.zeros([num, 128])
        name = []
        str_emb = np.empty([num, 128], dtype=float)

        # 获取所有行
        rows = self.readFronSqllite(self.DB_Path, self.sqlStr_SelectAll)
        lineIndex = 0
        if len(rows) == 0 or rows == '':
            emb_arr = 0
        else:
            while lineIndex < num:
                row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
                # print(row[0])
                name.append(row[0])  # 获取名字
                if row[1] == 0:
                    emb_arr[lineIndex] = np.full((1, 128), 10)
                else:
                    str_to_list = row[2].split()  # 以空格分割字符串
                    for i in range(128):
                        emb_arr[lineIndex][i] = float(str_to_list[i])  # 'list转ndarray:'，str->float
                lineIndex += 1

        return name, emb_arr, num


if __name__ == "__main__":
    fname = 'llf'
    str_emb = 'test'
    sql_insert_emb = 'insert into fileName(fName,falg,embadding) values ("' + fname + '",1,"' + str_emb + '");'
    sql_update_emb = 'update fileName set flag=1, embadding= "' + str_emb + '" where fName="' + fname + '";'
    print(sql_update_emb)
    # print(sql_insert_emb)
    # emb_arr = np.zeros([2, 128])
    # print(emb_arr)
    # emb_arr[0] = np.full((1, 128), 10)
    # print(emb_arr)
    # opSql = Operate_Sql()
    # opSql.insert_emb('llf', 's')

    # print(sql_emb[0])
    # list_emb=sql_emb
    # print(list_emb[0])

    # print(type(list))
    # print(list)
    # name = 123

    # print('select * from fileName where fName ="' + str(name) + '";')
#     pass
# name = "123"
# print('select * from fileName where fName ="' + name + '";')
#
# opSql.Select_All_Name()
#     opSql.Delete_File_Name('234')
# #
# #     #插入一条新记录
# name='111'
# flag = opSql.Select_Same_Name(name)
#     print('构建的插入语句：'+newname)
#     opSql.Insert_New_Name(newname)
#
#     # 查询总行数
#     num = opSql.Num_Row_All()
#     print('总行数为：', num,'\n')
#
#     # 查询第一条记录
#     opSql.SelcetFirst()
#
#     # 查询所有记录
#     opSql.Select_All()
#
#     # # 测试sql构建语句
#     # print(opSql.CreatSqlStr('llf'))
#     # print("insert into fileName(fName) values ('llf');")
#
