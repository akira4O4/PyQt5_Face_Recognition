import tensorflow as tf
import  numpy as np
import cv2

if __name__ == '__main__':
    img = cv2.imread('../src_img/nana.jpg')
    a=[]
    a.append(img)
    print(np.stack(a).shape)

