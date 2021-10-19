# -*- coding: utf-8 -*-
"""Task2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qf9s0DJ-Yrmt_quWOWRyjVM3zVAouKpd
"""

#FROM THE GIVEN 'IRIS' DATASET,PREDICT THE OPTIMUM NUMBER OF CLUSTERS AND REPRESENT IT VISUALLY.

#LOADING THE NECESSARY LIBRARIES
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Libraries Imported Successfully")

from sklearn import datasets

iris=datasets.load_iris()
df=pd.DataFrame(iris.data,columns=iris.feature_names)

df.head()

#DATASET SIZE
df.shape

#DATASET INFORMATION
df.info()

df.describe()

df.columns

#UNIVARIATE ANALYSIS
sns.distplot(df['sepal length (cm)'])
plt.xlabel('sepal length (cm)')
plt.ylabel('portability')
plt.title('Distribution plot')
plt.show()

sns.distplot(df['sepal width (cm)'])
plt.xlabel('sepal width (cm)')
plt.ylabel('portability')
plt.title('Distribution plot')
plt.show()

sns.distplot(df['petal length (cm)'])
plt.xlabel('petal length (cm)')
plt.ylabel('portability')
plt.title('Distribution plot')
plt.show()

sns.distplot(df['petal width (cm)'])
plt.xlabel('petal width (cm)')
plt.ylabel('portability')
plt.title('Distribution plot')
plt.show()

ax=sns.heatmap(df.corr(),annot=True)
bottom,top=ax.get_ylim()
ax.set_ylim(bottom+0.5,top-0.5)
plt.show()

#a.There is high positive correlation between:
#1.sepal length and petal width
#2.petal length and petal width
#3.sepal length and petal length
#b.There is a negative correlation between:
#1.sepal width and petal width
#2.sepal width and petal length
#3.sepal length and sepal width
sns.pairplot(df)
plt.show

#checking for the multicollinearity
import statsmodels.api as sm
Xc=sm.add_constant(df)

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif=[variance_inflation_factor(Xc.values,i) for i in range(Xc.shape[1])]
pd.DataFrame({'VIF':vif[1:]},index=df.columns)

#DATA PREPERATION
#1.STANDARD SCALING
#2.PCA APPLICATION
from sklearn.preprocessing import StandardScaler
ss=StandardScaler()

dfs=ss.fit_transform(df)
dfs=pd.DataFrame(dfs)
dfs.columns=df.columns
dfs.head()

from sklearn.decomposition import PCA
pca=PCA()

pca.fit(dfs)

pd.DataFrame({'Eigen_values':pca.explained_variance_,'proportion explained':pca.explained_variance_ratio_,'cumlative proprtion explained':np.cumsum(pca.explained_variance_ratio_)})

#The first 2PCs explain 95% of variation.Thus, considering only PC1 AND PC2
pca=PCA(0.95)

pca.fit(dfs)

pd.DataFrame({'Eigen_values':pca.explained_variance_,'proportion explained':pca.explained_variance_ratio_,'cumlative proprtion explained':np.cumsum(pca.explained_variance_ratio_)})

#The first 2PCs explain 95% of variation.Thus, considering only PC1 AND PC2
pca=PCA(0.95)

df_pca=pca.fit_transform(dfs)

cols=list(df.columns)

PCA_df=pd.DataFrame(pca.components_.T,index=cols,columns=['PC1','PC2']).reset_index().rename(columns={'index':'features'})
PCA_df

#kmeans clustering
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

kmeans=KMeans(random_state=0)

wcss=[]
sil_score=[]
for k in range(2,15):
  kmeans=KMeans(n_clusters=k)
  kmeans.fit(df_pca)
  wcss.append(kmeans.inertia_)
  sil_score.append(silhouette_score(df_pca,kmeans.labels_))
print(wcss,'\n',sil_score)

#Elbow plot
plt.plot(range(2,15),wcss)
plt.xlabel('no.of clusters')
plt.ylabel('wcss')
plt.show()

#sithoute score
plt.plot(range(2,15),sil_score)
plt.xlabel('no.of clusters')
plt.ylabel('sil_score')
plt.show()

kmeans=KMeans(n_clusters=3,n_init=15,random_state=0)

kmeans.fit(df_pca)

pd.Series(kmeans.labels_).value_counts()

plt.figure(figsize=[8,6])
sns.scatterplot(x=df_pca[:,0],y=df_pca[:,1],hue=kmeans.labels_,palette='spring')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('cluster visualization')
plt.show()

pd.DataFrame(kmeans.cluster_centers_)

df['labels']=kmeans.labels_

df.head()

df.groupby('labels').mean()

#with regars to 3 clusters,below are some observation
#1.The sepal length of flower in cluster 0 is largest
#2.The sepal width of flower cluster 2 is smallest
#3.The petal length of flower in cluster 0 is largest.This was to happen as sepal length and petal length are highly correlated.
#4.The petal width of flower in cluster 1 is the least