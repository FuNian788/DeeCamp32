import cv2
import numpy as np

class Basic():

    def __init__(self, 
                IMG_PATH = "G:/Deecamp/1.jpg", 
                ):
        self.IMG_PATH = IMG_PATH

    def CompressChannel(self):
        # 1.Compress the value of each channel from 256 kinds to 16 kinds.
        #   Disadvantages: There will be obvious edges in the continuous color block.
        img = cv2.imread(self.IMG_PATH)
        for i in range(len(img)):
            for j in range(len(img[0])):
                for k in range(len(img[0][0])):
                    img[i][j][k] = int(img[i][j][k] / 16) * 16
        cv2.imshow('compress image', img)
        cv2.waitKey(0)

    def AdaThreshold(self):
        # 2. Set an adaptive threshold for images with uneven brightness distribution.
        img = cv2.imread(self.IMG_PATH, 0)
        # Median filtering
        img = cv2.medianBlur(img,5)
        # Parameters in function: input image, max threshold, adaptive Method(mean/Gussian), threshold type, 
        #                         block size(odd number), constant(value = value - C)
        img1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
        img2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
        cv2.imshow('mean', img1)
        cv2.imshow('Gussian', img2)
        cv2.waitKey(0)

op = Basic()
# op.CompressChannel()
op.AdaThreshold()