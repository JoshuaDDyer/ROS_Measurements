# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 15:32:29 2019

@author: jd583
"""

import numpy as np
import tifffile
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import skimage.filters as skfilt
import csv
import os
import skimage
from skimage import morphology

input_folder_name='data' #input folder name
output_folder='tables' #output folder name

#find .tif files in input_folder_name, add to directory
li=os.listdir(input_folder_name)
filename_list=[]
for el in li:
    if el[-3:]=='tif':
	    filename_list.append(el)
print(filename_list)
# begin loop
for i,filename in enumerate(filename_list):
# load the data using tifffile, unlike when loading .czi files, no unnecessary
# dimensions are added, meaning that we do not need to use the .squeeze function. 
    print('processing file{}, this is file {} of {}'.format(filename,i+1,len(filename_list)))
    filepath = 'data/{}'.format(filename)
    mydata = tifffile.imread(filepath)
# show dimensions of loaded image
    print("The data we loaded has shape")
    print(mydata.shape)
# split channels 
    channel1 = mydata[0]
    channel2 = mydata[1]
    print("Channel 1 data has shape:", channel1.shape)
    print("Channel 2 data has shape:", channel2.shape)
# at this point extra filtering steps can be inserted. No filtering steps needed here.
    filtered1 = channel1
    filtered2 = channel2
# identify thresholding values using threshold_otsu only need to do this for channel 2 - channel 1 must remain with the original grey values
    threshold_value2 = skfilt.threshold_otsu(filtered2)
# apply threshold using comparison operator to generate a binary image named mask2
    mask2 = filtered2 >= threshold_value2
# generate labeled obects from mask 2 and print the number of objects identified - if number of objects is higher than 200 then image analysis is aborted
# using continue; usually this is due to ndi.label trying to identify objects in images without bacteria 
    labels2, num_objects2 = ndi.label(mask2)  
    if num_objects2>200:
        print('oh shit loads of stuff, abort this')
        continue

# remove all objects smaller than 10 connected pixels
    delfiltmask2 =  morphology.remove_small_objects(labels2,10,2)
    delfiltlabels2, delfilt_num_objects2 = ndi.label(delfiltmask2)
    print("Number of Mitochondrial objects following deletion", delfilt_num_objects2)
# create overlay images of each of the objects that pass the remove_small_objects screen onto the original image
    size=filtered2.shape
    plt.figure(
        "Mask 2 (slice 6)",
        figsize=(12, 12*size[0]/size[1]),
        dpi=size[1]/12,
    )
    plt.axes([0,0,1,1])
    plt.imshow(channel2, cmap='gray')
    plt.contour(delfiltmask2, levels=[0.5], colors=['b'])
    plt.savefig('{}_mask2.png'.format(filepath))
    plt.close()
    print("Created overlay images", flush=True)
# generate measurements of the corresponding area in channel 1 (filtered 1) as the label identified in channel 2 (filtered 2)   
    ROSmeasures = skimage.measure.regionprops (delfiltlabels2,filtered1)
    Bacteriameasures = skimage.measure.regionprops (delfiltlabels2,filtered2)
# make a list for ROSmeasures to be attached to
    ROSIntensityList = [['filename', 'label number', 'mean intensity', 'min intensity', 'max intensity', 'area of bacteria', 'mean intensity of bacteria']]
# for each label in ROSmeasures, add to ROSIntensityList
    for label in range(0, delfilt_num_objects2):
        labelmeasure = (filename, label, ROSmeasures[label].mean_intensity, ROSmeasures[label].min_intensity, ROSmeasures[label].max_intensity, ROSmeasures[label].area, Bacteriameasures[label].mean_intensity)
        ROSIntensityList.append(labelmeasure)
# write to CSV    
    file_out = open("{}/stats_table{}.csv".format(output_folder,filename), "w")
    writer = csv.writer(file_out)
    writer.writerows(ROSIntensityList)
    file_out.close()
# combine csvs