import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from statistics import mean

#store the x and y coordinate information of input data in array x and y. This also works with multi dimentional data
#don't forget to update dimension
x = [4, 5, 10, 4, 3, 11, 14 , 6, 10, 12, 69, 91, 66, 46, 40, 52, 49, 31, 36]
y = [21, 19, 24, 17, 16, 25, 24, 22, 21, 21, 73, 80, 4, 42, 21, 61, 33, 40, 47]
dimension = 2
#For example, if we are working with 4 dimensional data, just add z[] and w[], then use the code below.
#data = list(zip(x, y, z, w))
data = list(zip(x, y))

linkage_data = linkage(data, method='centroid', metric='euclidean')
#print(linkage_data)
similarity = []
for i in linkage_data:
    similarity.append(i[2])
diffSim = []
for d in range(len(similarity)):
    if d != 0:
        diffSim.append(similarity[d] - similarity[d-1])

#Tune this parameter to get the most accurate num_of_cluster
avg = mean(diffSim)
idx = []
door = 1.5
for a in range(len(diffSim)):
    if diffSim[a] > avg*door:
        idx.append(a)

num_of_cluster = len(idx) + 1

hierarchical_cluster = AgglomerativeClustering(n_clusters=num_of_cluster, affinity='euclidean', linkage='ward')
labels = hierarchical_cluster.fit_predict(data)

plt.scatter(x, y, c=labels)
plt.show()

#compute the centroid in each cluster
centroids = [[0]*dimension for x in range(num_of_cluster)]
c_num = 0
for i in range(0,len(data)):
    centroids[labels[i]][0] += data[i][0]
    centroids[labels[i]][1] += data[i][1]

count = 0
for group in centroids:
    group[0] = group[0] / (labels[np.where(labels==count)]).size
    group[1] = group[1] / (labels[np.where(labels == count)]).size
    count += 1

print (centroids)
#Finally the centroid of each cluster is stored in array centroids

#visulization codes to show dendrogram, uncomment to use.
#dendrogram(linkage_data)
#plt.show()