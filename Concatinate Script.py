# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 15:40:42 2019

@author: jd583
"""

import glob
import pandas as pd

path = r'\\isad.isadroot.ex.ac.uk\UOE\User\Desktop\ROS Measures Dev\tables'
filelist = glob.glob(path + "/*.csv")
print(filelist)
li = []
for filename in filelist:
    df = pd.read_csv(filename, index_col=None, header = 0)
    li.append(df)
frame = pd.concat(li, axis=0, ignore_index=True)
print(frame)
export_csv = frame.to_csv('_Concatinated Results.csv', index=None, header=True)
