import cv2
import pyautogui
import numpy as np
import datetime
import os





print("------------开始截图------------")
img = pyautogui.screenshot(region=[0, 0, 2500 ,1600]) 
#分别代表：左上角坐标，宽高
#对获取的图片转换成二维矩阵形式，后再将RGB转成BGR
#因为imshow,默认通道顺序是BGR，而pyautogui默认是RGB所以要转换一下，不然会有点问题
img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)



curr_time = datetime.datetime.now()
#时间转换成年月日格式
filename = str(datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S'))
#去除字符串空格
imgname1 = filename.replace(" ", "") + ".jpg"
imgname2 = imgname1.replace(":","-")
print("截图成功，文件名:" + imgname2) 
# cv2.imshow("截屏",img)
# cv2.haveImageWriter("b.jpg")
# cv2.imwrite(str(filename+".jpg"),img)
cv2.imwrite(imgname2,img)
cv2.destroyAllWindows()
print("------------截图完成------------")




