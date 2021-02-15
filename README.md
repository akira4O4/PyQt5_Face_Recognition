
 # 基于卷积神经网络的学生人脸识别考勤系统
 ## 上传前已经通过测试，希望各位认真查阅README，README中写了许多细节，不熟悉TensorFlow和python的请提前学习。欢迎给小星星。    
 ## 测试环境：
 >**1.Windows 10 Ubuntu 20.04**  
 >**2.TensorFlow1.15 GPU版本（没有GPU也可以，CPU版本会慢一些）**  
 >**3.PyQt5**  
 >**4.Sqlite3**  

 ## 使用的模型：
 ### MTCNN->人脸检测  
 ### FaceNet->人脸识别  

 ## 程序目录如下：
>**20170512-11-547下为FaceNet数据 这个数据太大无法上传，请到百度云下载**   
>**链接:https://** 
>**pan.baidu.**
>**com/s/1nMwbahnZ0ZgeIOO6UrATdw(请去掉空格)**
>**提取码：w3it  **    
>**align文件夹下为MTCNN模型数据**  
>**src文件夹下为所有主程序文件 SetUpMainWindow.py为启动文件**  
>**DB文件夹下为sqlite3数据库(文件夹里面是空的，运行主程序会自动创建,也可以手动创建，但是名字必须和DB_File里面写的一样)**  
>**ui_src文件夹下为ui设计文件和转码py文件**  
>**emb_img和src_img文件夹在程序运行时会自动创建（或者可以直接手动创建，两个都是空文件夹）**  


## 目录结构
![目录结构1](https://github.com/omega-Lee/PyQt5_Face_Recognition/blob/master/markdown_imgs/3.png)  


## DB目录讲解
>**StudentCheckWorkDB.db 为学生考勤数据表**  
>**StudentFaceDB.db 为学生人脸数据**  


## 操作步骤
0、SetUpMainWindow.py是主界面启动文件  
1、在数据库管理中添加用户，主要不要修改主键内容，修改主键内容会导致更新错误   
2、在主界面点击刷新，更新数据表  
3、选择学号ID  
4、打开摄像头->录入人脸  
5、点击生成模型（人脸模型生成过程线程会被阻塞，但是训练完成就没事了）    
5、开始检测  
  
## 软件界面细节  

![1](https://github.com/omega-Lee/PyQt5_Face_Recognition/blob/master/markdown_imgs/1.png) 

![2](https://github.com/omega-Lee/PyQt5_Face_Recognition/blob/master/markdown_imgs/2.png) 

