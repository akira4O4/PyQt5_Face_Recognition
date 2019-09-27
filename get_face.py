import tensorflow as tf
import numpy as np
import os
from scipy import misc
import copy
import facenet
import align.detect_face
import argparse


# 获取人脸部分
def align_data(image_path, imgae_size, gpu_memory_faction):
    minsize = 20
    threshhold = [0.6, 0.7, 0.7]
    factor = 0.709

    with tf.Graph().as_default():
        # per_process_gpu_memory_fraction指定了每个GPU进程中使用显存的上限，但它只能均匀地作用于所有GPU，无法对不同GPU设置不同的上限。
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_faction, allow_growth=True)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        # 加载mtcnn
        with sess.as_default():
            pnet, onet, rnet = align.detect_face.create_mtcnn(sess, None)

    temp_image_path = copy.copy(image_path)  # 浅拷贝文件目录
    image_list = []  # 图片列表
    for i_path in temp_image_path:
        img = misc.imread(os.path.expanduser(i_path), mode='RGB')  # 这样读出来的图片格式为numpy类型，后面就不需要再转换了
        img_size = np.asarray(img.shape)[0:2]  # 获取数据尺寸类型为ndarray
        print(i_path)

        # print('img.shape:', img.shape)
        # print('img_size:', img_size)

        bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, onet, rnet, threshhold, factor)
        if len(bounding_boxes) < 1:
            image_path.remove(i_path)
            print("无法检测到脸部，删除", i_path)
            continue

        # print('bounding_boxes:', bounding_boxes)
        det = np.squeeze(bounding_boxes[0, 0:4])  # 从数组的形状中删除单维度条目，即把shape中为1的维度去掉,数据降维
        # print('bounding_boxes降维:', det)
        # 切片操作需要整数类型

        bb = np.zeros(4, dtype=np.int32)
        bb[0] = det[0]
        bb[1] = det[1]
        bb[2] = det[2]
        bb[3] = det[3]
        cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]  # 四角坐标
        # print('cropped shape:', cropped.shape)
        # 改变图像大小并且隐藏归一化到0-255区间，根据cropped位置对原图重定义size
        aligned = misc.imresize(cropped, (imgae_size, imgae_size), interp='bilinear')  # 默认双线性插值
        prewhitened = facenet.prewhiten(aligned)  # 取出冗余数据
        image_list.append(prewhitened)
    images = np.stack(image_list)  # 沿着新轴连接数组的序列
    return images


def detection():
    img_src = '../src_img/'  # 图片输入目录
    img_path_set = []
    emb_file = '../emb_img'

    # 如果不存在这个目录就新建一个
    if (os.path.exists(emb_file) == False):
        os.mkdir(emb_file)

    # 获取目录下所有作品的路径
    for f in os.listdir(img_src):  # os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表
        one_img = os.path.join(img_src, f)
        # print('组合路径:', one_img)
        # print('单文件名:', f)
        img_path_set.append(one_img)
    print(img_path_set)
    images = align_data(img_path_set, 160, 1.0)

    # 保存切割好的图片
    count = 0
    for f in os.listdir(img_src):
        misc.imsave(os.path.join(emb_file, f), images[count])
        count = count + 1
        # 删除被剪裁的图片
        os.remove(os.path.join(img_src, f))


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_size', type=int, default=160)
    return parser.parse_args(argv)


def main(args):
    detection()


if __name__ == "__main__":
    # main(parse_arguments(sys.argv[1:]))
    detection()
