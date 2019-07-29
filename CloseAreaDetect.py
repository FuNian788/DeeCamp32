import cv2
import numpy as np
import random

class CloseAreaDetect():

    def __init__(self, 
                IMG_PATH = "G:/Deecamp/6.jpg", 
                Gray_Threshold = 200,
                Save_PATH = "G:/Deecamp/closeArea.jpg"
                ):
        self.IMG_PATH = IMG_PATH
        self.Gray_Threshold = Gray_Threshold
        self.Save_PATH = Save_PATH

    def CloseArea(self):
        # 1.Get grayscale for close area judgement. 
        img = cv2.imread(self.IMG_PATH)
        cv2.imshow('source image', img)
        cv2.waitKey(0)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2.Divide pixels to 2 categories through threshold (colors in original image may not be just balck and white).
        #   Gray image just has 2 channels.
        #   print(type(img)):np.adarray; So we use 'img.shape' instead of 'len(img[0][0])'.
        for i in range(gray_img.shape[0]):
            for j in range(gray_img.shape[1]):
                    # The threshold should be set manually.
                    gray_img[i][j] = 255 if gray_img[i][j]>=self.Gray_Threshold else 0
        cv2.imshow('gray image', gray_img)
        cv2.waitKey(0)

        # 3.Detect connected components and Mark one by one.
        _, labels = cv2.connectedComponents(gray_img, connectivity=8)
        AreaNum = np.max(labels)
        print("There are {} closed ares.".format(AreaNum) )

        # 4.Create a blank image and color each closed area.
        new_img = np.zeros(img.shape, np.uint8) 
        color_list = [(255,255,255)] * (AreaNum+1)
        # Create random color.
        for i in range(AreaNum):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color_list[i+1] = (r,g,b)
        # color each area.
        for i in range(len(labels)):
            for j in range(len(labels[0])):
                color = labels[i][j]
                for k in range(3):
                    new_img[i][j][k] =  color_list[color][k]
        cv2.imshow('closed-area image', new_img)
        cv2.imwrite(self.Save_PATH, new_img)
        cv2.waitKey(0)

op = CloseAreaDetect()
op.CloseArea()
