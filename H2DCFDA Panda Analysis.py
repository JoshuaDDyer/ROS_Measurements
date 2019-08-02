# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 15:45:25 2019

@author: jd583
"""

import pandas as pd
from pandas import io 
import csv

fileinput = r'\\isad.isadroot.ex.ac.uk\UOE\User\Desktop\ROS Measures Dev\_Concatinated Results.csv'
output_folder = r'\\isad.isadroot.ex.ac.uk\UOE\User\Desktop\ROS Measures Dev'
df = pd.read_csv(fileinput, header = 0)

"""
#way of showing column names
for col in df.columns: 
    print (col)
"""

#list of conditions
conditionlist = ["Con 1", "Con 2", "Con 3", "CYM 1", 
                 "CYM 2", "CYM 3", "sa +"]
#identifyer of condition we are using to standardize to
normalizedidentifyer = "sa +"
#identify mean and median of normalized conditions
normalize_df = df[df['filename'].str.contains(normalizedidentifyer)]
meannormalize_df = normalize_df.loc[:,"mean intensity"].mean()
mediannormalize_df = normalize_df.loc[:,"mean intensity"].median()
# empty list of summary stats
summarystatslist = [["condition", "mean-mean intensity", "normalized mean-mean intensity",
                     "median-mean intensity", "normalized median-mean intensity", "mean bacterial area",
                    "median bacterial area", "bacterial mean-mean intensity", "bacterial median-mean intensity"]]
for condition in conditionlist:
    statslist = []
    workingdf = df[df['filename'].str.contains(condition)]
    meanmeasure = workingdf.loc[:,"mean intensity"].mean()
    normalizedmean = (meanmeasure - meannormalize_df)
    medianmeasure = workingdf.loc[:,"mean intensity"].median()
    normalizedmedian = (medianmeasure - mediannormalize_df)
    meanbacteriasize = workingdf.loc[:,"area of bacteria"].mean()
    medianbacteriasize = workingdf.loc[:,"area of bacteria"].median()
    meanbacterialintensity = workingdf.loc[:,"mean intensity of bacteria"].mean()
    medianbacterialintensity = workingdf.loc[:,"mean intensity of bacteria"].median()
    measures = [condition,meanmeasure,normalizedmean,medianmeasure,normalizedmedian, 
                meanbacteriasize,medianbacteriasize, meanbacterialintensity, medianbacterialintensity]
    summarystatslist.append(measures)
print (summarystatslist)

# convert summarystatslist to a df
summarydf = pd.DataFrame.from_records(summarystatslist)
print(summarydf)
# perform 




file_out = open("{}/stats_table.csv".format(output_folder), "w")
writer = csv.writer(file_out)
writer.writerows(summarystatslist)
file_out.close()
