from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import imageio
import cv2
import tensorflow as tf
import numpy as np
import os

import facenet
import align.detect_face
from tools.sqlite_func import Sqlite_Func


# 交并比
def iou(a, b):
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])

    iou_x1 = np.maximum(a[0], b[0])
    iou_y1 = np.maximum(a[1], b[1])
    iou_x2 = np.minimum(a[2], b[2])
    iou_y2 = np.minimum(a[3], b[3])

    iou_w = iou_x2 - iou_x1
    iou_h = iou_y2 - iou_y1
    area_iou = iou_w * iou_h
    iou = area_iou / (area_a + area_b - area_iou)

    return iou


# 获取最大人脸索引
def max_face(area, position):
    max_face_position = []
    max_area_index = np.argmax(area)
    # print('最大面积索引：', np.argmax(area), '最大面积：', max(area))
    max_face_position = position[max_area_index]
    return max_face_position


class face():
    def __init__(self):
        self.init_mtcnn()
        self.train = False
        self.sqlite = Sqlite_Func()

    # 初始化MTCNN
    def init_mtcnn(self):
        print('初始化MTCNN')
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options,
                                                    log_device_placement=False))
            with sess.as_default():
                global pnet, rnet, onet
                pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)

    # 提前计算pre_embadding
    def init_pre_embdading(slef):
        print('初始化 Facenet')
        with tf.Graph().as_default():
            with tf.Session() as sess:
                model = '../20170512-110547/'
                facenet.load_model(model)
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                image = []
                nrof_images = 0
                global compare_emb, compare_num, all_obj_name
                emb_dir = '../emb_img'
                all_obj_name = []
                for i in os.listdir(emb_dir):
                    all_obj_name.append(i)
                    img = imageio.imread(os.path.join(emb_dir, i))
                    print('img.shape:', img.shape)
                    prewhitened = facenet.prewhiten(img)  # 预白化去除冗余信息
                    image.append(prewhitened)
                    nrof_images = nrof_images + 1
                # global compare_emb, compare_num
                images = np.stack(image)  # 沿着新轴连接数组的序列。
                feed_dict = {
                    images_placeholder: images,
                    phase_train_placeholder: False}
                # 计算对比图片embadding，embdadding是一个128维的张量
                compare_emb = sess.run(embeddings, feed_dict=feed_dict)
                print('compare_emb:', compare_emb)
                print('compare_emb_shape:', compare_emb.shape)
                compare_num = len(compare_emb)
                print("pre_embadding计算完成")
        return compare_emb, compare_num, all_obj_name  # 数据库embadding，人数，目录标签

    def main(self, face, checkwork):
        with tf.Graph().as_default():
            with tf.Session() as sess:
                model = '../20170512-110547/'
                facenet.load_model(model)
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

                '''
                id:学号
                compare_emb:特征值
                compare_num:数据库中的数据条数
                '''

                # 找到当表主键
                face_key_idx, face_key = self.sqlite.find_primary_key(self.sqlite.DB_STUDENTFACE_PATH, face)
                # cw_key_idx,cw_key=self.sqlite.find_primary_key(self.sqlite.DB_STUDENTCHECKWORK_PATH,checkwork)

                # 从数据库获取人脸数据
                cmd = self.sqlite.auto_select(face)
                rows = self.sqlite.executeCMD(self.sqlite.DB_STUDENTFACE_PATH, cmd)

                id = []

                num = len(rows)
                emb_idx = len(rows[0]) - 1

                compare_num = num
                compare_emb = np.zeros([num, 128])

                for lineIndex in range(num):
                    row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
                    id.append(row[face_key_idx])  # 获取id
                    emb_str = row[emb_idx]  # 获取一个组数据中的emb数据
                    if emb_str is None:
                        compare_emb[lineIndex] = np.full((1, 128), 10)
                    else:
                        str_list = emb_str.split(' ')  # 以空格分割字符串
                        if len(str_list) < 10:
                            continue
                        for i in range(128):
                            compare_emb[lineIndex][i] = float(str_list[i])  # 'list转ndarray:'，str->float

                capture = cv2.VideoCapture(0)
                cv2.namedWindow("face recognition", 1)

                while True:
                    ret, frame = capture.read()
                    frame = cv2.flip(frame, 1)
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # 识别框
                    cv2.putText(frame, 'Identification Box', (200, 90), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                1, (0, 0, 255),
                                thickness=2,
                                lineType=1)
                    cv2.rectangle(frame, (150, 100), (490, 380), (165, 245, 25), 2)
                    BOX = [150, 100, 490, 380]

                    # 获取视频流中的最大人脸 判断标识 bounding_box crop_image
                    mark, bounding_box, crop_image = self.load_and_align_data(rgb_frame, 160)

                    '''
                    范围限制
                    '''
                    if mark:
                        if bounding_box[0] < 75:
                            mark = False
                            # print('left')
                        if bounding_box[2] > 565:
                            mark = False
                            # print('right')

                    if mark:
                        # print('计算视频帧的embadding')
                        emb = sess.run(embeddings, feed_dict={images_placeholder: crop_image,
                                                              phase_train_placeholder: False})
                        pre_person_num = len(emb)
                        find_obj = []
                        # print('识别到的人数:', pre_person_num)
                        cv2.putText(frame,
                                    'Press esc to exit',
                                    (10, 30),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                    1, (0, 0, 255),
                                    thickness=1,
                                    lineType=1)
                        # 逐一对比
                        for i in range(pre_person_num):  # 为bounding_box 匹配标签
                            dist_list = []  # 距离列表

                            for j in range(compare_num):
                                # 求误差(欧氏距离)
                                dist = np.sqrt(np.sum(np.square(np.subtract(emb[i, :], compare_emb[j, :]))))
                                dist_list.append(dist)
                                # 求视频帧和对比图直接最小的差值，即表示为最相似的图片
                                min_value = min(dist_list)
                                # print("最小差值：", min_value)
                            if min_value > 0.65:
                                find_obj.append('Unknow')
                            else:
                                dist_index = dist_list.index(min_value)
                                find_obj.append(id[dist_index])

                        # 在frame上绘制边框和文字
                        cv2.rectangle(frame,
                                      (bounding_box[0], bounding_box[1]),
                                      (bounding_box[2], bounding_box[3]),
                                      (0, 255, 0), 1, 8, 0)
                        cv2.putText(frame, str(find_obj[0]),
                                    (bounding_box[0], bounding_box[1]),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                    1,
                                    (0, 0, 255),
                                    thickness=2,
                                    lineType=2)

                    # 将学号插入到选择的考勤表中
                    if find_obj[0] != "Unknow":
                        self.sqlite.update_checkwork(self.sqlite.DB_STUDENTCHECKWORK_PATH, checkwork, find_obj[0])
                    cv2.imshow('face recognition', frame)
                    key = cv2.waitKey(3)
                    if key == 27:
                        break
                capture.release()
                cv2.destroyWindow("face recognition")

    def load_and_align_data(self, img, image_size):

        minsize = 20
        threshold = [0.6, 0.7, 0.7]
        factor = 0.709
        bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
        Index = []  # 序列
        Area = []  # 面积
        Position = []  # 坐标

        # print('len(bounding_boxes):', len(bounding_boxes))

        # 如果未发现目标 直接返回
        if len(bounding_boxes) < 1:
            # print('没有发现人脸')
            return False, 0, 0

        for i, face_position in enumerate(bounding_boxes):
            face_position = face_position.astype(int)
            w = face_position[2] - face_position[0]
            h = face_position[3] - face_position[1]
            S = w * h
            # print('第:', i)
            # print('w:', w)
            # print('h:', h)

            Index.append(i)
            Area.append(S)
            Position.append(face_position)

        max_face_position = max_face(Area, Position)

        # print('bbox:', (max_face_position[0], max_face_position[1]),
        #       (max_face_position[2], max_face_position[3]))

        # 裁剪
        temp_crop = img[max_face_position[1]:max_face_position[3], max_face_position[0]:max_face_position[2], :]

        if max_face_position[0] < 75:  # 左边
            return False, 0, 0

        if max_face_position[2] > 565:  # 右边
            return False, 0, 0

        if max_face_position[1] < 75:  # 上面
            return False, 0, 0

        aligned = cv2.resize(temp_crop, (image_size, image_size),
                             interpolation=cv2.INTER_CUBIC)
        face_out = facenet.prewhiten(aligned)
        crop_image = []
        crop_image.append(np.stack(face_out))
        return True, max_face_position, crop_image  # mark标记位置，回归边框，切割图片


if __name__ == '__main__':
    face_test = face()
    face_test.main('cs172', 'cs172')
