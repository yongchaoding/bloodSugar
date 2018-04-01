# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 15:43:10 2018

@author: YongchaoDing
"""

import cv2
import numpy as np
import xlrd
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy import optimize  

FrameHZ = 30;
Size = 100
X_start = 900
Y_start = 300

def  readExcel(file):
    File=xlrd.open_workbook(file)
    # sheet 0 information
    sheet=File.sheet_by_index(0)
    # time is col0 and force is col1
    time=sheet.col_values(0)
    force=sheet.col_values(1)
    #print (time)
    #print (force)
    return time, force

def reformForceData(force):
    force_array = [];
    for i in range(len(force)):
        for j in range(FrameHZ):
            force_array.append(force[i]);
    return force_array, len(force_array);

def dataCombine(force_array, b_array, g_array, r_array, force_len, numFrame):
    dataLen = min(force_len, numFrame);
    force_array = force_array[:dataLen - 1];
    b_array = b_array[:dataLen - 1];
    g_array = g_array[:dataLen - 1];
    r_array = r_array[:dataLen - 1];
    CombinedData = [force_array, b_array, g_array, r_array];
    # print(CombinedData);
    return CombinedData;

def DrawPlot(DataArray):
    plt.figure(1);
    plt.plot(DataArray[0], DataArray[1], '.');
    
    plt.figure(2);
    plt.plot(DataArray[0], DataArray[2], '.');
    
    plt.figure(3);
    plt.plot(DataArray[0], DataArray[3], '.');
    plt.show();

def f_1(x, A, B):
    return A*x + B

def curveFit(DataArray):
    A1, B1 = optimize.curve_fit(f_1, DataArray[0], DataArray[1])[0];
    plt.figure(1);
    plt.plot(DataArray[0], DataArray[1], '.');
    x1 = np.arange(200, 400, 1)  
    y1 = A1*x1 + B1  
    plt.plot(x1, y1, "blue") 
    return A1, B1
    
def openVideo(file):
    cap = cv2.VideoCapture(file);
    # shape = (int(VideoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(VideoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
    Num_frame = 1;
    ret, frame  =cap.read();
    shape = frame.shape
    while(cap.isOpened()):
        ret, frame  =cap.read();
        if ret == False:
            break;
        Num_frame += 1
    cap.release()
    cap = cv2.VideoCapture(file);
    return cap, Num_frame, shape

def resizeFrame(frame, shape, coefficient):
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    newFrame = cv2.resize(frame, (int(shape[1] * coefficient), int(shape[0] * coefficient)), interpolation=cv2.INTER_CUBIC)
    return newFrame

def showFrame(name, frame):
    cv2.imshow(name, frame);
    cv2.waitKey(20);
    #if(keycode == 27):
    #   break;

def frameThreshold(frame):
    res = cv2.threshold(frame,30,255,cv2.THRESH_BINARY)
    #res = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,3,5)
    return res

def centerDetection(frame):
    circles= cv2.HoughCircles(frame,cv2.HOUGH_GRADIENT,1,300,param1=50,param2=15, minRadius=200,maxRadius=400)
    if circles is None:
        print("circles is Zero")
    else:
        print(len(circles[0]))
    return circles

def drawCircle(frame, circles):
    if not circles is None:
        for circle in circles[0]:
            #坐标行列
            x=int(circle[0])
            y=int(circle[1])
            #半径
            r=int(circle[2])
            #在原图用指定颜色标记出圆的位置
            frame=cv2.circle(frame,(x,y),r,(0,0,255),-1)
    return frame

def ROI(frame, x_s, x_e, y_s, y_e):
    imageROI = frame[y_s:y_e,x_s:x_e];
    cv2.rectangle(frame,(x_s,y_s),(x_e,y_e),(0,0,0),1)
    return imageROI, frame

def rgbDivide(frame):
    b = cv2.split(frame)[0];
    g = cv2.split(frame)[1];
    r = cv2.split(frame)[2];
    b_sum = math.log(b.mean()) * Size * Size;
    g_sum = math.log(g.mean()) * Size * Size;
    r_sum = math.log(r.mean()) * Size * Size;
    return b_sum, g_sum, r_sum

if __name__ == '__main__':
    # read video and excel file
    _, force = readExcel('../../ForceData/ForceTest.xlsx');
    force_array, force_len = reformForceData(force);
    cap, numFrame, shape = openVideo('../../VideoData/VideoTest.MOV');
    # init some params
    frame_num= 0;
    b_array = [];
    g_array = [];
    r_array = [];
    while(cap.isOpened()):
        frame_num = frame_num + 1;
        ret, frame  =cap.read()
        if ret == False:# or frame_num > 100:
            break;
        originImage = frame.copy()
        frame = resizeFrame(frame, shape, 0.5)
        _, grayFrame = frameThreshold(frame)

        # detect center auto
        #circles = centerDetection(grayFrame)
        #circleFrame = drawCircle(grayFrame, circles)
        imageROI, frame = ROI(originImage, int(X_start-Size/2), int(X_start + Size/2), int(Y_start-Size/2), int(Y_start + Size/2));
        b,g,r = rgbDivide(imageROI);

        b_array.append(b);
        g_array.append(g);
        r_array.append(r);
        print("ID: %d b is %d, g is %d, r is %d\n"  %(frame_num, b, g, r));
        #showFrame('Frame', frame);
        #showFrame('ROI', imageROI);

    CombinedData = dataCombine(force_array, b_array, g_array, r_array, force_len, frame_num);
    DataArray=np.array(CombinedData);
    DataArray.sort();
    curveFit(DataArray);
    #DrawPlot(DataArray);
    
    print("len of force is %d, rgb is %d\n" %(len(force_array), len(b_array)));
    dataframe = pd.DataFrame({'force':CombinedData[0],'b':CombinedData[1],'g':CombinedData[2],'r':CombinedData[3]});
    dataframe.to_csv("VideoTest.csv",index=False,sep=',');


