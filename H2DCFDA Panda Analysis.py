"""
Created on Fri Aug  2 15:45:25 2019

@author: jd583
"""

import pandas as pd
from pandas import io 
import csv

fileinput = '_Concatinated Results.csv'
output_folder = 'stats'
df = pd.read_csv(fileinput, header = 0)

"""
#way of showing column names
for col in df.columns: 
    print (col)
"""
#list of conditions - note that SA + represents the H2DCFDA -ve control - couldn't find it anyother way!
conditionlist = ["Con 1", "Con 2", "Con 3", "CYM 1", 
                 "CYM 2", "CYM 3", "sa + h2dcfda - 1","sa + h2dcfda - 2"]

#identifyer of condition we are using to standardize to - we have two normalization controls in this experiment so
#have adjusted the code below to reflect this
normalizedidentifyer1 = "sa + h2dcfda - 1"
normalizedidentifyer2 = "sa + h2dcfda - 2"
# note use of regex=False; having regex = True prevented identifying the normalized conditions
# tbh not entirely sure why. 
normalized1 = df[df['filename'].str.contains(normalizedidentifyer1, regex = False)]
normalized2 = df[df['filename'].str.contains(normalizedidentifyer2, regex = False)]

meannormalized1 = normalized1.loc[:,"mean intensity"].mean()
meannormalized2 = normalized2.loc[:,"mean intensity"].mean()
print ('meannormalized1 {}'.format(meannormalized1))
print ('meannormalized2 {}'.format(meannormalized2))
mediannormalized1 = normalized1.loc[:,"mean intensity"].median()
mediannormalized2 = normalized2.loc[:,"mean intensity"].median()
print ('mediannormalized1 {}'.format(mediannormalized1))
print ('mediannormalized2 {}'.format(mediannormalized2))

#identify mean and median of normalized  conditions by adding the two normalized
# and dividing by two

meannormalize_df = (meannormalized1 + meannormalized2) / 2
mediannormalize_df = (mediannormalized1 + mediannormalized2) / 2

print('mediannormalize_df={}'.format(mediannormalize_df))
print('meannormalize_df={}'.format(meannormalize_df))


# empty list of summary stats
summarystatslist = [["condition", "mean-mean intensity", "normalized mean-mean intensity",
                     "median-mean intensity", "normalized median-mean intensity", "mean bacterial area",
                    "median bacterial area", "bacterial mean-mean intensity", "bacterial median-mean intensity"]]
for condition in conditionlist:
    statslist = []
    workingdf = df[df['filename'].str.contains(condition, regex = False)]
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
print (summarydf)

#Export summarydf
exportdftocsv = summarydf.to_csv("{}/summaryResults.csv".format(output_folder))

#file_out = open("{}/stats_table.csv".format(output_folder), "w")
#writer = csv.writer(file_out)
#writer.writerows(summarystatslist)#file_out.close()