import cv2
import numpy as np

class Basic():

    def __init__(self, 
                IMG_PATH = "G:/Deecamp/1.jpg", 
                Save_PATH = "G:/Deecamp/1/gradient.jpg"
                ):
        self.IMG_PATH = IMG_PATH
        self.Save_PATH = Save_PATH


    def CompressChannel(self, img):
        # 1.Compress the value of each channel from 256 kinds to 16 kinds.
        #   Disadvantages: There will be obvious edges in the continuous color block.
        for i in range(len(img)):
            for j in range(len(img[0])):
                for k in range(len(img[0][0])):
                    img[i][j][k] = int(img[i][j][k] / 16) * 16
        cv2.imshow('compress image', img)
        cv2.waitKey(0)
        return img


    def AdaThreshold(self, img):
        # 2.Set an adaptive threshold for images with uneven brightness distribution.
        if (len(img.shape)==3):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
        # NOTE: this function has 2 output images, so choose one to return.
        # return img1
        # return img2


    def Opening(self, img, ErodeIter = 1, DilateIter = 1, KernelSize = 5):
        # 3.We always erode --> dilate to remove samll background-objects/noises, fill some edges.
        #   Sometimes we should set iterations instead of using 'cv2.morphologyEx', same as below.
        #   Be careful of the size of the kernel, same as below.
        if (len(img.shape)==3):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("source image", img)
        cv2.waitKey(0)
        kernel = np.ones((KernelSize, KernelSize), np.uint8)

        for i in range(ErodeIter):
            img = cv2.erode(img, kernel)
            cv2.imshow("erosion" + str(i), img)
            cv2.waitKey(0)

        for i in range(DilateIter):
            img = cv2.dilate(img, kernel)
            cv2.imshow("dilation" + str(i), img)
            cv2.waitKey(0)

        # opening = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
        return img


    def Closing(self, img, ErodeIter = 1, DilateIter = 1, KernelSize = 5):
        # 4.We always dilate --> erode to splice break edges.
        if (len(img.shape)==3):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("source image", img)
        cv2.waitKey(0)
        kernel = np.ones((KernelSize, KernelSize), np.uint8)

        for i in range(DilateIter):
            img = cv2.dilate(img, kernel)
            cv2.imshow("dilation" + str(i), img)
            cv2.waitKey(0)

        for i in range(ErodeIter):
            img = cv2.erode(img, kernel)
            cv2.imshow("erosion" + str(i), img)
            cv2.waitKey(0)

        # closing = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
        return img


    def Gradient(self, img, SaveImage = False):
        # 5. gradient = dilation - erosion, which is some kind of edge.
        if (len(img.shape)==3):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((3,3), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
        if(SaveImage):
            cv2.imwrite(self.Save_PATH, img)
        cv2.imshow("gradient", img)
        cv2.waitKey(0)
        return img

        


# test code 
if __name__=="__main__":
    op = Basic()
    img = cv2.imread(op.IMG_PATH)
    img = op.CompressChannel(img)
    # img = op.AdaThreshold(img)
    img = op.Opening(img)
    img = op.Closing(img)
    img = op.Gradient(img, SaveImage = True)