import os
import shutil

class File_Operate():
    def __init__(self):
        self.path = "../faces/"

    def Create_File(self, filename):
        path = self.path + filename
        print(path)
        # 去除首位空格
        path = path.strip()
        # 判断路径是否存在
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            # print(path + ' 创建成功\n')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            # print(path + ' 目录已存在\n')
            return False

    def Delete_File(self, filename):
        path = self.path + filename
        path = path.strip()

        shutil.rmtree(path)
        # os.rmdir(path)

if __name__ == "__main__":
    fo = File_Operate()
    fo.Create_File('new')
    # fo.Delete_File('123')