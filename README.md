# Deecamp
### Group32: image-based closed edge map generation.   
#### Contributors: Zhangli Zhou, Yang Jiao, Zixiao Pan, Zexian Li.  

In order to reduce unnecessary repetitive work, we open some code, which mainly consist of traditional methods in computer vision.  
For related deep-learning methods, we hope to get your suggestions, including but not limited to GAN, K-means, Style migration, Semantic segmentation and so on.  
Wish for your pull request. If you find more traditional methods, please contact us as well.    

1.['CannyOperator.py'](https://github.com/FuNian788/Deecamp32/blob/master/CannyOperator.py) includes two main operators.    
The function 'StaticCanny' can perform a Canny operation on the input image, but you need to set the low / high thresholds manually.  
The function 'DynamicCanny' can dynamically modify the thresholds through a trackbar.  
The function 'SplitMerge' splits the source image to 3 channels, finds each image's edge through Canny, then bitwise AND and merge 3 new edges, which may get good edges.  
By the way, don't forget to change the image's path and static thresholds in the function 'init'. The same below.  

2.['CloseAreaDetect.py'](https://github.com/FuNian788/Deecamp32/blob/master/CloseAreaDetect.py) can detect all closed areas in the input images and output its number.   
You should set a threshold for the grayscale to get better performance, change the threshold until the grayscale image has a sharp edge.   
In order to visually see the closed area, we randomly color all areas and then save the image.  
We hope that this Op can help you evaluate the quality of the edge extraction algorithm.    
We get some perfect results, so if the result you get is a mess, check your code and don't sleep.  
Some samples are shown as below(source image, gray image and the result).   
<img width="250" height="250" alt="source image" src="https://github.com/FuNian788/Deecamp32/raw/master/img/CloseAreaDetect/source.jpg"/>
<img width="250" height="250" alt="source image" src="https://github.com/FuNian788/Deecamp32/raw/master/img/CloseAreaDetect/gray.jpg"/> 
<img width="250" height="250" alt="source image" src="https://github.com/FuNian788/Deecamp32/raw/master/img/CloseAreaDetect/result.jpg"/>  

3.['Basic.py'](https://github.com/FuNian788/Deecamp32/blob/master/Basic.py) includes some basic operations for edge extraction. We hope you can use these methods to get good results. (If one method doesn't work, try another one, or you can average the results of all methods.)      
We collected some basic algorithms based on python-opencv, which help to extract the edges.  
The functions are introduced as below.  
(1) CompressChannel: compress the value of each channel from 256 kinds to 16 kinds, which improves the contrast of the image, but may lead to some obvious edges in the continuous color block.  
(2) AdaThreshold: For images with uneven brightness distribution, we can use adaptive methods(mean/Gussian) to find suitable threshold.  
(3) Opening: We always erode --> dilate to remove samll background-objects/noises, fill some edges. We set iterations instead of using 'cv2.morphologyEx' here, and please be careful of the size of the kernel, same as below.  
(4) Closing: We always dilate --> erode to splice break edges, eliminate holes inside the foreground.  
(5) Gradient: Gradient = Dilation - Erosion, which is some kind of edge. Surprisingly, this method works very well in some images.   

#### All the code has detailed comments，if you don't understand, just google it.

