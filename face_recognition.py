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
import sqlite3_op


# 获取最大人脸索引
def max_face(area, position):
    max_face_position = []
    max_area_index = np.argmax(area)
    print('最大面积索引：', np.argmax(area), '最大面积：', max(area))
    max_face_position = position[max_area_index]
    return max_face_position


class face():
    def __init__(self):
        self.init_mtcnn()
        self.train = False
        self.opsql = sqlite3_op.Operate_Sql()
        # if self.train == False:
        #     self.init_pre_embdading()

    # 初始化MTCNN
    def init_mtcnn(self):
        print('初始化MTCNN')
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
            sess = tf.Session(
                config=tf.ConfigProto(
                    gpu_options=gpu_options,
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

    def main(self, stop):
        with tf.Graph().as_default():
            with tf.Session() as sess:
                model = '../20170512-110547/'
                facenet.load_model(model)
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                all_obj_name, compare_emb, compare_num = self.opsql.get_sql_emb()
                print(compare_emb)
                capture = cv2.VideoCapture(0)
                cv2.namedWindow("face recognition", 1)

                while True:
                    ret, frame = capture.read()
                    frame = cv2.flip(frame, 1)
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # 获取视频流中的人脸 判断标识 bounding_box crop_image
                    mark, bounding_box, crop_image = self.load_and_align_data(rgb_frame, 160)

                    if mark:
                        print('计算视频帧的embadding')
                        emb = sess.run(embeddings, feed_dict={
                            images_placeholder: crop_image,
                            phase_train_placeholder: False})
                        print("emb shape:", emb.shape)
                        pre_person_num = len(emb)
                        find_obj = []
                        print('识别到的人数:', pre_person_num)
                        cv2.putText(frame, 'Press esc to exit', (10, 30),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                    1, (0, 0, 255),
                                    thickness=1,
                                    lineType=1)
                        for i in range(pre_person_num):  # 为bounding_box 匹配标签
                            dist_list = []  # 距离列表
                            if compare_num == 0:
                                min_value = 1
                            else:
                                for j in range(compare_num):
                                    # 求误差(欧氏距离)，存储每个embadding-compare_embadding对应的distance
                                    dist = np.sqrt(
                                        np.sum(np.square(np.subtract(emb[i, :], compare_emb[j, :]))))
                                    dist_list.append(dist)
                                # 求视频帧和对比图直接最小的差值，即表示为最相似的图片
                                min_value = min(dist_list)
                                print("最小差值：", min_value)
                            if min_value > 0.65:
                                find_obj.append('Unknow')
                            else:
                                # 从dist.list里面选择最接近的index并在obj_name里面查找对应的name
                                find_obj.append(
                                    all_obj_name[dist_list.index(min_value)])

                        # 在frame上绘制边框和文字
                        if bounding_box[0] > 10 and bounding_box[1] > 10:
                            cv2.rectangle(frame,
                                          (bounding_box[0], bounding_box[1]),
                                          (bounding_box[2], bounding_box[3]),
                                          (0, 255, 0), 1, 8, 0)
                            cv2.putText(frame, find_obj[0],
                                        (bounding_box[0], bounding_box[1]),
                                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                        1,
                                        (0, 0, 255),
                                        thickness=2,
                                        lineType=2)
                    cv2.imshow('face recognition', frame)
                    key = cv2.waitKey(3)
                    if stop:
                        break
                    if key == 27:
                        break
                capture.release()
                cv2.destroyWindow("face recognition")

    def load_and_align_data(self, img, image_size):
        minsize = 20

        threshold = [0.6, 0.7, 0.7]
        factor = 0.709

        # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5,
        #                  interpolation=cv2.INTER_AREA)

        # bounding_boxes shape:(1,5)  type:np.ndarray
        bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
        Index = []  # 序列
        Area = []  # 面积
        Position = []  # 坐标

        print('len(bounding_boxes):', len(bounding_boxes))

        # 如果未发现目标 直接返回
        if len(bounding_boxes) < 1:
            print('没有发现人脸')
            return 0, 0, 0

        for i, face_position in enumerate(bounding_boxes):
            face_position = face_position.astype(int)
            w = face_position[2] - face_position[0]
            h = face_position[3] - face_position[1]
            S = w * h
            print('第:', i)
            print('w:', w)
            print('h:', h)

            Index.append(i)
            Area.append(S)
            Position.append(face_position)

        max_face_position = max_face(Area, Position)

        print('bbox:', (max_face_position[0], max_face_position[1]),
              (max_face_position[2], max_face_position[3]))

        # 裁剪
        temp_crop = img[max_face_position[1]:max_face_position[3], max_face_position[0]:max_face_position[2], :]
        aligned = cv2.resize(temp_crop, (image_size, image_size),
                             interpolation=cv2.INTER_CUBIC)
        face_out = facenet.prewhiten(aligned)
        crop_image = []
        crop_image.append(np.stack(face_out))

        # cv2.imshow('face_out', face_out)
        # cv2.imshow('crop_image', crop_image)
        # print('face_out', face_out.shape)
        # print('crop_image', crop_image.shape)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return True, max_face_position, crop_image  # mark标记位置，回归边框，切割图片


if __name__ == '__main__':
    face_test = face()
    face_test.main(False)
    # img = cv2.imread('../src_img/me.jpg')
    # face_test.load_and_align_data(img, 160)
