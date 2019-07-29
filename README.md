# Deecamp
### Group32: image-based closed edge map generation.   
Contributors: Zhangli Zhou, Yang Jiao, Zixiao Pan, Zexian Li.  

In order to reduce innecessary repetitive operations, we open some code.  

1.['CannyOperator'](https://github.com/FuNian788/Deecamp32/blob/master/CannyOperator.py) includes two main operations.    
The function 'StaticCanny' can perform a Canny operation on the input image, but you need to set the low / high thresholds manually.  
The function 'DynamicCanny' can dynamically modeify the thresholds through a trackbar.  
By the way, don't forget to change the image's path and static thresholds in the function 'init'. The same below.  

2.[CloseAreaDetect](https://github.com/FuNian788/Deecamp32/blob/master/CloseAreaDetect.py) can detect all closed areas in the input images and output its number.   
You should set a threshold for the grayscale to get better performance, change the threshold until the grayscale image has a sharp edge.   
In order to visually see the closed area, we randomly color all areas and then save the image.  
We hope that this Op can help you evaluate the quality of the edge extraction algorithm.    
We get some perfect results, so if the result you get is a mess, check your code and don't sleep.  
Some samples are shown as below(source image, gray image and the result).   
<img width="250" height="250" alt="source image" src="https://github.com/FuNian788/Deecamp32/raw/master/img/CloseAreaDetect/source.jpg"/>
<img width="250" height="250" alt="source image" src="https://github.com/FuNian788/Deecamp32/raw/master/img/CloseAreaDetect/gray.jpg"/> 
<img width="250" height="250" alt="source image" src="https://github.com/FuNian788/Deecamp32/raw/master/img/CloseAreaDetect/result.jpg"/>  

3.['Basic'](https://github.com/FuNian788/Deecamp32/blob/master/Basic.py) includes some basic operations for edge extraction.  

