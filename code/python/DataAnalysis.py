# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 12:50:37 2018

@author: YongchaoDing
"""

import scanVideo
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy import optimize  

def csvRead(fileName):
    force = [];
    g_light = [];
    b_light = [];
    r_light = [];
    fileName = reconstructName(fileName);
    print(fileName);
    c=open(fileName,"r")
    read=csv.reader(c)
    count = 0;
    for line in read:
        count = count + 1;
        if count != 1:
            force.append(line[1]);
            g_light.append(line[2]);
            b_light.append(line[0]);
            r_light.append(line[3]);
    return force, g_light, b_light, r_light;
    
def reconstructName(eachlist):
    eachlistName = eachlist + ".csv"
    return eachlistName;

if __name__ == '__main__':
    force = [];
    light_g = [];
    listFile = scanVideo.readListFile("lists.txt");

    for i in range(len(listFile)):
       force, g_light, _,_ = csvRead(listFile[i]);
       plt.plot(force, g_light, '.');
    plt.show();
       
       