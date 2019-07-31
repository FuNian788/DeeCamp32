# For extracting better edges, we combine several traditional algorithms.
# We provide more flexible paramters.

import cv2
import numpy 
import Basic
import CloseAreaDetect
import CannyOperator

if __name__ == "__main__":
    OpBasic = Basic.Basic(IMG_PATH = "G:/Deecamp/1.jpg", 
                          Save_PATH = "G:/Deecamp/test/gradient.jpg")
    OpCanny = CannyOperator.ImageChange(Static_Low_Threshold = 30, 
                                        Static_High_Threshold = 80)
    OpDetect = CloseAreaDetect.CloseAreaDetect(Save_PATH = "G:/Deecamp/test/closeArea.jpg",
                                               Gray_Threshold = 50)

    img = cv2.imread(OpBasic.IMG_PATH)
    # 1. Do 'Gradient'(dilation - erosion).
    img = OpBasic.Gradient(img, KernelSize = 3, SaveImage = False)
    # 2. Do 'Canny'. Press 'Space' to move on.
    # img = OpCanny.StaticCanny(img)
    img = OpCanny.DynamicCanny(img)
    # 3. Detect closed areas.
    img = OpDetect.CloseArea(img, GrayWhiteChange = True, SaveImage = False)

