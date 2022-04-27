import fileinput

inputs = []
animal_name_list = []
line_count = 0
train_data = []
test_data = []

# Read data from input
for line in fileinput.input():
    if line_count != 0: 
        clean_line = line.strip()
        splitted_line = clean_line.split(",")
        animal_name_list.append(splitted_line[0])
        if splitted_line[-1] == '-1':
            test_data.append(splitted_line[1:])
        else:
            train_data.append(splitted_line[1:])
        inputs.append(clean_line)
    line_count += 1

def train_class(dataset):
    separated = dict()
    for i in dataset:
        if i[-1] not in separated:
            separated[i[-1]] = list()
        separated[i[-1]].append(i[:-1])
    return separated

def prob_py(sample):
    count = len(sample)
    py = count + 0.1 / (train_sample_num + 0.1 * num_classes)
    return py

def conditional_prob_pxy(sample):
    pxy = []
    conditional_prob = []
    for col in range(15):
        if col == 12:
            count_0 = count_2 = count_4 = count_6 = count_8 = count_5 = 0 
            for row in sample:
                if row[col] == '0':
                    count_0 += 1
                elif row[col] == '2':
                    count_2 += 1
                elif row[col] == '4':
                    count_4 += 1
                elif row[col] == '6':
                    count_6 += 1
                elif row[col] == '8':
                    count_8 += 1
                else:
                    count_5 += 1
            row_conditional_prob = ((count_0 + 0.1)/(len(sample) + 0.6), (count_2 + 0.1)/(len(sample) + 0.6), (count_4 + 0.1)/(len(sample) + 0.6),
               (count_5 + 0.1)/(len(sample) + 0.6), (count_6 + 0.1)/(len(sample) + 0.6), (count_8 + 0.1)/(len(sample) + 0.6))
        else:
            count_0 = 0
            count_1 = 0
            for row in sample:
                if row[col] == '0':
                    count_0 += 1
                elif row[col] == '1':
                    count_1 += 1
                row_conditional_prob = ((count_0 + 0.1)/(len(sample) + 0.2), (count_1 + 0.1)/(len(sample) + 0.2))
        conditional_prob.append(row_conditional_prob)
    
    return conditional_prob

def train(training_labelled):
    model = dict()
    for class_value, rows in training_labelled.items():
        pxy = conditional_prob_pxy(rows)
        py = prob_py(rows)
        model[class_value] = [pxy, py]
    return model

# Return the prediction possibilities for a given sample
def single_prob_test_data(model, item):
    probabilities = dict()
    for class_name, class_probs in model.items():
        py = class_probs[1] # initial py 
        probabilities[class_name] = py
        for i in range(15):
            idx = int(item[i])
            if i == 12:
                idx = translate_leg(int(item[i]))
            probabilities[class_name] *= class_probs[0][i][idx]
    
    return probabilities

def translate_leg(ipt):
    if ipt == 0:
        return 0
    elif ipt == 2:
        return 1
    elif ipt == 4:
        return 2
    elif ipt == 5:
        return 3
    elif ipt == 6:
        return 4 
    else:
        return 5
    
# Predict the category for a given sample
def predict(model, sample):
    probabilities = single_prob_test_data(model, sample)
    max_prob = 0
    returned_class= None
    
    for class_name, probability in probabilities.items():
        if probability > max_prob:
            max_prob = probability
            returned_class = class_name

    return returned_class

# main function
train_sample_num = len(train_data)
training_labelled_class = train_class(train_data)
num_classes = len(training_labelled_class.keys())
model = train(training_labelled_class)
for i in test_data:
    print(predict(model, i[:-1]))