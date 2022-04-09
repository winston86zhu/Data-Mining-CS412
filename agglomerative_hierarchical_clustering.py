import fileinput

count = 0 
lines = 0
clusters = 0
method = 0

data = dict()
index = 0

"""
Referred to the methodology mentioend in this post: https://www.datanovia.com/en/lessons/cluster-validation-statistics-must-know-methods/

However, the about post is written in R 
"""

# Read input and store data to a dict 
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
    
def distance(x, y):
    all_dist = []
    for item in range(len(x)):
        one_dist = (x[item]-y[item])**2
        all_dist.append(one_dist)
    return sum(all_dist)**(1/2)

def cluster_dist(pt1, pt2):
    point_dists = []
    for item1 in pt1:
        for item2 in pt2: 
            if item1 != item2:
                point_dists.append(dist[item1][item2])
    if method == 0:
        return_dist = min(point_dists)
    elif method == 1:
        return_dist = max(point_dists)
    else:
        return_dist = sum(point_dists)/len(point_dists)
    return return_dist


# initiate distance matrix
# initiate cluster assignment {point_index: cluster_assignment}
dist = []
cluster_dict = dict()
for i in range(lines):
    new = []
    for j in range(lines):
        new.append(0) 
    dist.append(new)

    
for i in data.keys():
    cluster_dict.update({i:[i]})
    for j in data.keys():
        if i!=j:
            dist[i][j] = distance(data.get(i), data.get(j))
    


cur_num_cluster = lines
while int(cur_num_cluster)>int(clusters):
    
    # calculate distance between clusters 
    key_list = (list(cluster_dict.keys()))
    cluster_distance = []
    for key1 in key_list:
        for key2 in key_list:
            if key2 > key1:
                cluster_distance.append((key1, key2, 
                                         cluster_dist(cluster_dict.get(key1),
                                                      cluster_dict.get(key2))))
    
    # find 2 closest clusters
    min_dist = float("inf")
    min_dist_pair_cluster = {}
    for pair_cluster_dist in cluster_distance:
        if (pair_cluster_dist[2] < min_dist):
            min_dist = pair_cluster_dist[2]
            min_dist_pair_cluster = pair_cluster_dist

    
    # merge 2 closest cluster
    # https://stackoverflow.com/questions/19773669/python-dictionary-replace-values
    merge_row_one = min_dist_pair_cluster[0] #[3,4,5]
    merge_row_two = min_dist_pair_cluster[1] #[1,2]
    new_cluster = cluster_dict.get(merge_row_one)+cluster_dict.get(merge_row_two)
    cluster_dict.pop(merge_row_two)
    cluster_dict.update({merge_row_one:new_cluster})

    cur_num_cluster -= 1


# Print result
cluster_result = []
for index, keys in cluster_dict.items():
    for key in keys:
        cluster_result.append([index, key])

sorted_result = sorted(cluster_result, key=lambda x:x[1])

for item in sorted_result:
    print(item[0])

