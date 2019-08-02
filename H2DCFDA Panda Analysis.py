"""
Created on Fri Aug  2 15:45:25 2019

@author: jd583
"""

import pandas as pd
from pandas import io 
import csv

fileinput = '_Concatinated Results.csv'
output_folder = r'E:\CYM-5442 H2DCFDA S. aureus ROS Assays\2019-07-09 S. aureus H2DCFDA Rep 1\2019-07-09 Analysis'
df = pd.read_csv(fileinput, header = 0)

"""
#way of showing column names
for col in df.columns: 
    print (col)
"""

#list of conditions - note that SA + represents the H2DCFDA -ve control - couldn't find it anyother way!
conditionlist = ["Con 1", "Con 2", "Con 3", "CYM 1", 
                 "CYM 2", "CYM 3", "SA +"]
#identifyer of condition we are using to standardize to
normalizedidentifyer = "SA +"
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
# change SA+ to SA+H3DCFDA to better identify control condition
summarydf_nameadjusted = summarydf.replace('SA +' , 'SA + H2DCFDA -ve')
print(summarydf_nameadjusted)

exportdftocsv = summarydf_nameadjusted.to_csv("{}/summaryResults.csv".format(output_folder))

#now find a way to get averages of Con and CYM into a final DF

#file_out = open("{}/stats_table.csv".format(output_folder), "w")
#writer = csv.writer(file_out)
#writer.writerows(summarystatslist)#file_out.close()
