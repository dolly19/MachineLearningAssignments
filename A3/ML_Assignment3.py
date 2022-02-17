# -*- coding: utf-8 -*-
"""ML_Assignment3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16exjboxw_mbe7DdNvk1ah8wT7lGACkgH
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/gdrive')
# %cd '/content/gdrive/MyDrive/ML datasets/Assignment3'
# %ls

import warnings
warnings.filterwarnings('ignore')

#importing all needed libraries
!pip install pyclustering

from math import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pyclustering.cluster.kmedians import kmedians
from sklearn.decomposition import PCA
from pyclustering.cluster import cluster_visualizer
from tqdm import tqdm

"""#1. Preprocessing"""

# loading dataset
data = pd.read_csv('population.csv')

"""Question 1.1"""

#replacing ? with NaN values
data = data.replace(" ?",np.nan)

"""Question 1.2"""

#counting null values in each column
data.isnull().sum()

#40% is 79809.2
#dropping columns whose null values count is more than 79809.2
data = data.drop(['MIGMTR1','MIGMTR3','MIGMTR4','MIGSUN'],axis=1)

"""#2. Feature Analysis

Question 2.1
"""

#plotting for categorical values
data["ACLSWKR"].hist(bins=9, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("ACLSWKR")

data["AHGA"].hist(bins=17, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AHGA")

data["AHSCOL"].hist(bins=10, figsize=(6, 4),rwidth=0.8)
plt.title("AHSCOL")

data["AMARITL"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AMARITL")

data["AMJIND"].hist(bins=24, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AMJIND")

data["AMJOCC"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AMJOCC")

data["ARACE"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("ARACE")

data["AREORGN"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AREORGN")

data["ASEX"].hist(figsize=(6, 4))
plt.title("ASEX")

data["AUNMEM"].hist(figsize=(6, 4))
plt.title("AUNMEM")

data["AUNTYPE"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AUNTYPE")

data["AWKSTAT"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AWKSTAT")

data["FILESTAT"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("FILESTAT")

data["GRINREG"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("GRINREG")

data["GRINST"].hist(bins=50, figsize=(15, 6), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("GRINST")

data["HHDFMX"].hist(bins=38, figsize=(15, 6), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("HHDFMX")

data["HHDREL"].hist(bins=15, figsize=(8, 6), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("HHDREL")

data["MIGSAME"].hist(bins=15, figsize=(6, 4), rwidth=0.8)
plt.title("MIGSAME")

data["PARENT"].hist(bins=15, figsize=(10, 4), rwidth=0.8)
plt.title("PARENT")

data["PEFNTVTY"].hist(bins=42, figsize=(10, 4), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("PEFNTVTY")

data["PEMNTVTY"].hist(bins=42, figsize=(10, 4), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("PEMNTVTY")

data["PENATVTY"].hist(bins=42, figsize=(10, 4), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("PENATVTY")

data["PRCITSHP"].hist(bins=20, figsize=(18, 4), rwidth=0.8)
plt.title("PRCITSHP")

data["VETQVA"].hist(bins=10, figsize=(6, 4), rwidth=0.8)
plt.title("VETQVA")

#plots of numerical columns
data.hist(bins=15, figsize=(25, 20), rwidth=0.8)

"""Question 2.2"""

#dropping columns by analysing above plots 
def dropCommonFeature(df):
  drop_col = []
  n = len(df)
  for (columnName, columnData) in df.iteritems():
      most_frequent = df[columnName].value_counts().iloc[0]
      if most_frequent/n > 0.78:
          drop_col.append(columnName)

  df.drop(columns = drop_col , inplace = True)
  return df , drop_col

data, drop_col = dropCommonFeature(data)
print(drop_col)

data.shape

"""#3. Imputation, Bucketization, One-Hot Encoding

Question 3.1

we can see from the below result we don't have any missing values as all the columns that have missing values are dropped in the above steps
"""

data.isnull().sum()

"""Question 3.2"""

#Bucketize Numerical features
def bucketize(data):
  data['AAGE']= pd.cut(data['AAGE'],4,labels=['children','youth','adults','seniors'])
  data['WKSWORK'] = pd.cut(data['WKSWORK'],4,labels=['less','more','average','more than average'])
  data['ADTIND'] = pd.cut(data['ADTIND'],52,labels= range(0,52))
  data['ADTOCC'] = pd.cut(data['ADTOCC'],47,labels= range(0,47))
  data['NOEMP'] = pd.cut(data['NOEMP'],7,labels= range(0,7))
  data['VETYN'] = pd.cut(data['VETYN'],3,labels= range(0,3))
  data['YEAR'] = pd.cut(data['YEAR'],2,labels= [95,94])
  return data

data = bucketize(data)

"""Question 3.3"""

def encoding(data):
  #One hot encode features
  encoded_data = pd.get_dummies(data)

  #number of columns
  print(encoded_data.shape)

  #converting encoded_data to encoded_data_array as we have to pass this in pca 
  encoded_data_array = encoded_data.to_numpy()

  return encoded_data_array

encoded_data_array = encoding(data)

"""#Feature Transformation step"""

#fit PCA
pca = PCA()
pca.fit_transform(encoded_data_array)

#analyzing cumulative variance vs number of components
total_var = pca.explained_variance_.sum()
k=0
current_var = 0
#counting feature if cumulative varience is less than 85%
while current_var/total_var < 0.85:
  current_var += pca.explained_variance_[k]
  k+=1

print("features",k)

#fitting PCA again with the number of components that is chosen k=37.
pca = PCA(n_components=k)
train = pca.fit_transform(encoded_data_array)

train.shape

"""#4. Clustering

Question 4.1
"""

#Apply K-median clustering with varying values of k in the range [10,24]
median = list()
instances = list()

for x in tqdm(range(10,25)):
  array = train[0:x]
  model = kmedians(train, array)
  model.process()
  median.append(model.get_medians())
  instances.append(model)

k_values = []
for x in range(10,25):
  k_values.append(x)

print(k_values)

#function to calculate Within-Cluster Sum of Square
def Cal_WCSS(k_vals , k_median_instances , train):
    avg_dist = []
    for k in range(len(k_vals)):
        total_dis = 0
        model = k_median_instances[k]
        cluster = model.get_clusters()
        median = model.get_medians()
        for i in range (len(cluster)):
            dis = 0
            cl = cluster[i]
            m = median[i]
            for idx in cl:
                dis = dis + (((train[idx] - m)**2).sum())
            dis = dis/2*len(cl)
            total_dis += dis
        avg_dist.append(total_dis)

    return np.array(avg_dist)

avg_distance = Cal_WCSS(k_values,instances,train)

#function to plot elbow graph
def elbowCurve(avg_distance):
  plt.figure()
  plt.plot(range(10,25),avg_distance, 'b-')
  plt.xlabel("number of clusters")
  plt.ylabel("avg centroid distance")
  plt.title("Avg centroid distance vs K-medians")
  plt.legend()
  plt.show()

elbowCurve(avg_distance)

"""Question 4.2

By analyzing the graph we can see that the graph gradually changes at point k=19 and thus creating an elbow shape. From this point, the graph starts to move somewhat parallel to the X-axis. Thus, k=19 is the optimal K value or an optimal number of clusters.

Question 4.3
"""

#Applying K-median clustering with the best value chosen above k = 19
intial = train[0:19]
final_model = kmedians(train, intial)
final_model.process()

final_model

"""#5. Handling more_than_50k data

1. Preprocessing
"""

#loading the dataset
data1 = pd.read_csv('more_than_50k.csv')

#replacing ? with NaN values
data1 = data1.replace(" ?",np.nan)

data1.shape

#counting null values in each column
data1.isnull().sum()

#40% is 1432
#dropping columns whose null values count is more than 1432
data1 = data1.drop(['MIGMTR1','MIGMTR3','MIGMTR4','MIGSUN'],axis=1)

"""2. Feature Analysis"""

#plotting for categorical value
data1["ACLSWKR"].hist(bins=9, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("ACLSWKR")

data1["AHGA"].hist(bins=17, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AHGA")

data1["AHSCOL"].hist(bins=10, figsize=(6, 4),rwidth=0.8)
plt.title("AHSCOL")

data1["AMARITL"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AMARITL")

data1["AMJIND"].hist(bins=24, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AMJIND")

data1["AMJOCC"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AMJOCC")

data1["ARACE"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("ARACE")

data1["AREORGN"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AREORGN")

data1["ASEX"].hist(figsize=(6, 4))
plt.title("ASEX")

data1["AUNMEM"].hist(figsize=(6, 4))
plt.title("AUNMEM")

data1["AUNTYPE"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AUNTYPE")

data1["AWKSTAT"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("AWKSTAT")

data1["FILESTAT"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("FILESTAT")

data1["GRINREG"].hist(bins=15, figsize=(6, 4),rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("GRINREG")

data1["GRINST"].hist(bins=50, figsize=(15, 6), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("GRINST")

data1["HHDFMX"].hist(bins=38, figsize=(15, 6), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("HHDFMX")

data1["HHDREL"].hist(bins=15, figsize=(8, 6), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("HHDREL")

data1["MIGSAME"].hist(bins=15, figsize=(6, 4), rwidth=0.8)
plt.title("MIGSAME")

data1["PARENT"].hist(bins=15, figsize=(10, 4), rwidth=0.8)
plt.title("PARENT")

data1["PEFNTVTY"].hist(bins=42, figsize=(10, 4), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("PEFNTVTY")

data1["PEMNTVTY"].hist(bins=42, figsize=(10, 4), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("PEMNTVTY")

data1["PENATVTY"].hist(bins=42, figsize=(10, 4), rwidth=0.8)
plt.xticks(rotation='vertical')
plt.title("PENATVTY")

data1["PRCITSHP"].hist(bins=20, figsize=(18, 4), rwidth=0.8)
plt.title("PRCITSHP")

data1["VETQVA"].hist(bins=10, figsize=(6, 4), rwidth=0.8)
plt.title("VETQVA")

#plots of numerical columns
data1.hist(bins=15, figsize=(25, 20), rwidth=0.8)

#dropping columns same as dataset1
data1 = data1.drop(['AHRSPAY', 'AHSCOL', 'ARACE', 'AREORGN', 'AUNMEM', 'AUNTYPE', 'CAPGAIN', 'CAPLOSS', 'DIVVAL', 'GRINREG', 'GRINST', 'PEFNTVTY', 'PEMNTVTY', 'PENATVTY', 'PRCITSHP', 'SEOTR', 'VETQVA'],axis=1)

data1.shape

"""3. Imputation, Bucketization, One-Hot Encoding"""

data1.isnull().sum()

#Bucketize Numerical features
data1 = bucketize(data1)

#encoding the data
encoded_data1_array = encoding(data1)

""" Feature Transformation step"""

#fitting PCA with the number of components that is chosen k=37 above
train1 = pca.fit_transform(encoded_data1_array)

"""4. Clustering"""

train1.shape

prediction_50k = final_model.predict(train1)

"""#6. Compare more_than_50k data with Population Data

Question 6.1
"""

#proportion for general population
clusters = final_model.get_clusters()
proportion_pop = list()
for i in range(19):
    proportion_pop.append(len(clusters[i]) / len(train))
proportion_pop = np.array(proportion_pop)

#proportion of more_than_50k data
cluster_50k = np.zeros(19 , dtype = int)
for i in range(len(prediction_50k)):
    cluster_50k[prediction_50k[i]] +=1
proportion_50k = cluster_50k/cluster_50k.sum()

#plotting proportion v/s k clusters
fig = plt.subplots(figsize =(8, 6))
barWidth = 0.25
br1 = np.arange(19)
br2 = [x + barWidth for x in br1]
plt.bar(br1 , proportion_pop, label = 'population',width = barWidth)
plt.bar(br2 , proportion_50k, label = 'more than 50k',width = barWidth)
plt.xticks([r + barWidth for r in range(19)],br1)

plt.title('proportion v/s clusters')
plt.ylabel('proportion')
plt.xlabel('cluster number')
plt.legend(loc="upper right")

"""Question 6.2"""

diff = proportion_pop - proportion_50k
diff2 = proportion_50k - proportion_pop

for x in range(1,20):
  print("Difference","      ",x,"       ",diff[x-1])

plt.plot(diff)

"""By analysing the graph cluster 19 seems to be over represented as it has a very large differnce as compare to more than 50k cluster 19"""

for x in range(1,20):
  print("Difference2","      ",x,"       ",diff2[x-1])

plt.plot(diff2)

"""By analysing the graph cluster 2 and 4 seems to be over represented as it has a very large differnce as compare to population cluster 2 and 4

Question 6.3
"""

