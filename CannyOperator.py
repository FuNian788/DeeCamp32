import cv2
import numpy as np
 
class ImageChange():

    def __init__(self, 
                IMG_PATH = "G:/Deecamp/1.jpg", 
                Static_Low_Threshold = 30, 
                Static_High_Threshold = 80,
                Dynamic_Low_Threshold = 0, 
                Dynamic_High_Threshold = 0,
                ):
        self.IMG_PATH = IMG_PATH
        self.Static_Low_Threshold = Static_Low_Threshold
        self.Static_High_Threshold = Static_High_Threshold
        self.Dynamic_Low_Threshold = Dynamic_Low_Threshold
        self.Dynamic_High_Threshold = Dynamic_High_Threshold


    '''static Canny operator'''
    def StaticCanny(self, img):
        # Canny needs grayscale images 
        if (len(img.shape)==3):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Gaussian smoothing for noise reduction
        # aperture size = 3
        img = cv2.GaussianBlur(img,(3,3), 0)
        canny = cv2.Canny(img, self.Static_Low_Threshold, self.Static_High_Threshold)

        cv2.imshow('Canny', canny)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return img


    '''Use canny to change the image while high threshold is 3*low_threshold.'''
    def DynamicCannyBase(self, low_threshold):
        img = cv2.imread(self.IMG_PATH)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny = cv2.GaussianBlur(gray_img, (3,3), 0)
        # low_threshold comes from the function 'DynamicThresholdTrackbar'.
        canny = cv2.Canny(canny, low_threshold, 3*low_threshold)
        # add some colours to edges from 'canny'image.
        new_canny = cv2.bitwise_and(img, img, mask = canny)
        cv2.imshow('canny demo', new_canny)
        # if cv2.waitKey(0) == 27:
        #    cv2.destroyAllWindows()


    '''Get dynamic threshold(low) for dynamic canny function.'''
    def DynamicThresholdTrackbar(self):
        # Create a window.
        cv2.namedWindow('Dynamic Canny')
        # Create trackbars for low threshold and return it for fuction 'DynamicCanny'.
        cv2.createTrackbar('Low threshold', 'Dynamic Canny', self.Dynamic_Low_Threshold, 200, self.DynamicCannyBase) 
        # cv2.createTrackbar('High threshold', 'Dynamic Canny', self.Dynamic_High_Threshold, 500, self.DynamicCanny)


    def nothing():
        pass
    
    
    def DynamicCanny(self, img, kernel_size = 3):
        cv2.namedWindow('thresholds')
        # function 'nothing' means pass.
        cv2.createTrackbar('low threshold', 'thresholds', 0, 200, self.nothing)
        cv2.createTrackbar('high threshold', 'thresholds', 0, 1000, self.nothing)
        while(1):
            self.Dynamic_Low_Threshold = cv2.getTrackbarPos('low threshold', 'thresholds')
            self.Dynamic_High_Threshold = cv2.getTrackbarPos('high threshold', 'thresholds')
            img = cv2.imread(self.IMG_PATH, 0)
            img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
            img = cv2.Canny(img, self.Dynamic_Low_Threshold, self.Dynamic_High_Threshold)
            img = cv2.bitwise_and(img, img, mask = img)
            cv2.imshow('canny demo', img)
            stop = cv2.waitKey(1)
            # press Esc to exit.
            if stop == 27:
                break
            # Press 'Space' to save parameters and go on.
            if stop == 32:
                return img
        cv2.destroyAllWindows()


    '''Split the source image to 3 channels(r,g,b), find each image's edge through Canny,
            then bitwise AND and merge 3 new edges.'''
    def SplitMerge(self, img):
        b = cv2.Canny(cv2.GaussianBlur(img[:,:,0], (3,3), 0), self.Static_Low_Threshold, self.Static_High_Threshold)
        g = cv2.Canny(cv2.GaussianBlur(img[:,:,1], (3,3), 0), self.Static_Low_Threshold, self.Static_High_Threshold)
        r = cv2.Canny(cv2.GaussianBlur(img[:,:,2], (3,3), 0), self.Static_Low_Threshold, self.Static_High_Threshold)

        BitwiseAnd = cv2.bitwise_and(b,g,r)
        cv2.imshow('BitwiseAnd', BitwiseAnd)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return img

# test code 
if __name__=="__main__":
    op = ImageChange()
    img = cv2.imread(op.IMG_PATH)
    # 1.Static Canny
    '''
    img = op.StaticCanny(img)
    '''
    # 2.Dynamic Canny for one threshold.
    '''
    op.DynamicThresholdTrackbar()
    op.DynamicCannyBase(0)
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
    '''
    # 3. Dynamic Canny for two threshold.
    
    img = op.DynamicCanny(img)
    
    # 4. Canny for each channel and then bitwise AND.
    '''
    img = op.SplitMerge(img)
    '''