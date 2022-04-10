import math
import fileinput
from collections import Counter

data = dict()
index = 0
ground = []
predicted = []

# The first number is the ground-truth cluster label of the i-th instance, and the second number is the predicted cluster label of the i-th instance
for line in fileinput.input():
    line_split = line.split()
    data.update({index: [int(line_split[0]), int(line_split[1])]})
    ground.append(line_split[0])
    predicted.append(line_split[1])
    index +=1
ground_counter = Counter(ground)
predicted_counter = Counter(predicted)

def cluster_to_probablity(lst):
    all_cluster_set = set(lst)
    list_len = len(lst)
    counter_dict = Counter(lst)
    prob_list = []
    for value in counter_dict.values():
        prob_list.append(value / list_len)
    return prob_list
    

def mutual_information():
    
    total_len = index
    cluster1_counter = ground_counter
    cluster2_counter = predicted_counter
    
    data_pair = [(value[0],value[1]) for value in data.values()]
    data_pair_counter = Counter(data_pair)
    
    returned_value = 0
    for pair, occurance in data_pair_counter.items():
        i, j = pair # i is the ground-truth (0th column); j is the predicted cluster (1th column)
        pij = occurance/total_len
        pc = cluster1_counter[str(i)]/total_len
        pg = cluster2_counter[str(j)]/total_len
        returned_value += pij * math.log(pij/(pc*pg), 2)
    return returned_value

def entropy(cluster):
    prob = cluster_to_probablity(cluster)
    return_value = 0
    for value in prob:
        return_value -= value * math.log(value, 2)
    return return_value

# Referred to this post regarding calculating union and intersection
# https://www.learndatasci.com/glossary/jaccard-similarity/
# No code was copy and pasted 
def jaccard_coefficient():
    total_len = index
    cluster1_counter = predicted_counter
    cluster2_counter = ground_counter
    
    data_pair = [(value[0],value[1]) for value in data.values()]
    data_pair_counter = Counter(data_pair)
    
    # step 1: true positive
    true_positive = 0
    for pair, occurance in data_pair_counter.items():
        true_positive += (occurance * (occurance - 1)) / 2
    
    # step 2: false positive
    false_positive = 0
    for pair, occurance in cluster2_counter.items():
        false_positive += occurance * (occurance - 1) / 2
    false_positive -= true_positive 
    
    # step 3: false negative
    false_negative = 0
    for pair, occurance in cluster1_counter.items():
        false_negative += occurance * (occurance - 1) / 2
    false_negative -= true_positive 
    
    # step 4: return jaccard
    return true_positive / (true_positive + false_negative + false_positive)


# normalized-mutual-information
# Referred to math formula: https://luisdrita.com/normalized-mutual-information-a10785ba4898
def nmi(cluster1,cluster2):
    # Step 1: Calculate mutual info
    mi = mutual_information()
    
    # step 2: calculate entropy
    entropy1 = entropy(cluster1)
    entropy2 = entropy(cluster2)
    
    return mi/math.sqrt(entropy1 * entropy2)

print("%.3f" % round(nmi(ground, predicted), 3) + " " + "%.3f" % round(jaccard_coefficient(), 3))
