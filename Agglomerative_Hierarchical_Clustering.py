# 5 2 0
# 150.8586 -33.5872
# 144.7548 -37.7099
# 31.4162 -28.3352
# 113.8974 30.5215
# -110.5385 41.7794

import fileinput

count = 0 
lines = 0
clusters = 0
method = 0

data = dict()
idx = 0
def distance(x, y):
    dist = [(x[i]-y[i])**2 for i in range(len(x)-1)]
    return sum(dist)**(1/2)

def cluster_dist(pt1, pt2):
    dist_list = [dist[element1][element2] for element1 in pt1 for element2 in pt2 if element1 != element2]
    if method==0:
        temp = min(dist_list)
    elif method==1:
        temp = max(dist_list)
    else:
        temp = sum(dist_list)/len(dist_list)
    return temp

for line in fileinput.input():
    if count == 0:
        arg_list = line.split()
        lines = arg_list[0]
        clusters = arg_list[1]
        method = arg_list[2]
    else:
        lon, lat = line.split(' ')
        data.update({idx: [float(lon), float(lat)]})
        idx +=1
        
    count += 1

print(data)
print(data.keys())

# initiate distance matrix
dist = []
for i in range(count):
    new = []
    for j in range(count):
        new.append(0) 
    dist.append(new)

# fill-in dist matrix
for i in data.keys():
    for j in data.keys():
        if i!=j:
            dist[i][j] = distance(data.get(i), data.get(j))

    
print(dist)

cluster_dict = dict()
for key in data.keys():
    cluster_dict.update({key:[key]})

print(cluster_dict)

n = count
while int(n)>int(clusters):
    # calculate distance between clusters
    sorted_keys = sorted(list(cluster_dict.keys()))
    dist_list = [ (key1, key2, cluster_dist(cluster_dict.get(key1),cluster_dict.get(key2))) for idx1, key1 in enumerate(sorted_keys)
                 for idx2, key2 in enumerate(sorted_keys[idx1+1:])]
    
    i, j, _ = min(dist_list, key= lambda t: t[2] if t[2] else float('inf'))

    # get new cluster and remove previous ones
    new_cluster = cluster_dict.get(i)+cluster_dict.get(j)
    temp = cluster_dict.pop(i)
    temp = cluster_dict.pop(j)
    cluster_dict.update({i:new_cluster})

    # update cluster list
    new_cluster_dict = dict()
    idx = 0
    for key, item in cluster_dict.items():
        new_cluster_dict.update({idx:item})
        idx +=1
    cluster_dict = new_cluster_dict

    n = len(cluster_dict)

# print out results after transforming to list
result_list = [[key, element] for key, item in cluster_dict.items() for element in item]
arg_sort_idx = sorted(range(len(result_list)), key=list(zip(*result_list))[1].__getitem__)
clusters = list(zip(*result_list))[0]

for idx in arg_sort_idx:
    print(clusters[idx])
