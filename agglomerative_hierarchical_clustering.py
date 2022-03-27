import fileinput

count = 0 
lines = 0
clusters = 0
method = 0

data = dict()
index = 0

def distance(x, y):
    all_dist = []
    for item in range(len(x)):
        one_dist = (x[item]-y[item])**2
        all_dist.append(one_dist)
    return sum(all_dist)**(1/2)

def cluster_dist(pt1, pt2):
    # dist_list = [dist[element1][element2] for element1 in pt1 for element2 in pt2 if element1 != element2]
    point_dists = []
    for item1 in pt1:
        for item2 in pt2: 
            if item1 != item2:
                point_dists.append(dist[item1][item2])
    if method==0:
        return_dist = min(point_dists)
    elif method==1:
        return_dist = max(point_dists)
    else:
        return_dist = sum(point_dists)/len(point_dists)
    return return_dist

for line in fileinput.input():
    if count == 0:
        arg_list = line.split()
        lines = int(arg_list[0])
        clusters = int(arg_list[1])
        method = int(arg_list[2])
    else:
        x1, y1 = line.split(' ')
        data.update({index: [float(x1), float(y1)]})
        index +=1
        
    count += 1


# initiate distance matrix
dist = []
for i in range(lines):
    new = []
    for j in range(lines):
        new.append(0) 
    dist.append(new)

# fill-in dist matrix
for i in data.keys():
    for j in data.keys():
        if i!=j:
            dist[i][j] = distance(data.get(i), data.get(j))


cluster_dict = dict()
for key in data.keys():
    cluster_dict.update({key:[key]})


cur_num_cluster = lines
while int(cur_num_cluster)>int(clusters):
    
    # calculate distance between clusters 
    sorted_keys = sorted(list(cluster_dict.keys()))
    cluster_distance = []
    for key1 in sorted_keys:
        for key2 in sorted_keys:
            if key2 > key1:
                cluster_distance.append((key1, key2, 
                                         cluster_dist(cluster_dict.get(key1),cluster_dict.get(key2))))
    
    i, j, _ = min(cluster_distance, key= lambda t: t[2] if t[2] else float('inf'))

    # merge 2 closest cluster
    new_cluster = cluster_dict.get(i)+cluster_dict.get(j)
    temp = cluster_dict.pop(i)
    temp = cluster_dict.pop(j)
    cluster_dict.update({i:new_cluster})

    # update cluster list
    new_cluster_dict = dict()
    for index, item in enumerate(cluster_dict.items()):
        new_cluster_dict.update({index:item[1]})
    cur_num_cluster = len(new_cluster_dict)
    cluster_dict = new_cluster_dict

    
# print out results after transforming to list
# print("final cluster : \n")
# print(cluster_dict)
cluster_result = []
for index, keys in cluster_dict.items():
    for key in keys:
        cluster_result.append([index, key])

sorted_result = sorted(cluster_result, key=lambda x:x[1])

for item in sorted_result:
    print(item[0])

