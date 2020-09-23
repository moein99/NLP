from collections import Set
import math

train_data_addr = "../../../ClsData/train.txt"
test_data_addr = "../../../ClsData/test.txt"

testcase_train_data_addr = "../../../ClsData/TestCase.Train.txt"
testcase_test_data_addr = "../../../ClsData/TestCase.Test.txt"



output = "../{type}.output.txt"
eval = "../{type}.report.txt"
output_addr = ""
eval_addr = ""


def read_data_lines(addr):
    with open(addr, 'r', encoding="UTF-8") as file:
        return [i.split() for i in file.readlines()]


def train(train_data):
    classes = []
    vocabulary = set()
    classes_names = set()
    for line in train_data:
        class_name = line[0]
        if class_name not in classes_names:
            classes_names.add(class_name)
            classes.append({})
            index = max(label_to_index.values()) + 1 if len(label_to_index) != 0 else 0
            label_to_index[class_name] = index
            index_to_label[index] = class_name
        label_index = label_to_index[line[0]]
        for i in range(1, len(line)):
            token = line[i]
            vocabulary.add(token)
            if token in classes[label_index]:
                classes[label_index][token] += 1
            else:
                classes[label_index][token] = 1
    classes = compute_frequencies(classes, vocabulary)
    return classes


def compute_frequencies(classes, vocabulary):
    classes_word_count = []
    vocab_length = len(vocabulary)
    for label in sorted(label_to_index.values()):
        classes_word_count.append(sum(classes[label].values()))
        classes[label]["UNK"] = 1 / (classes_word_count[label] + vocab_length)
    for word in vocabulary:
        for label in sorted(label_to_index.values()):
            if word in classes[label]:
                classes[label][word] = (classes[label][word] + 1) / (classes_word_count[label] + vocab_length)
    return classes


def test(test_data, classes):
    results = []
    for line in test_data:
        temp = [math.log10(0.5)] * len(classes)
        for i in range(1, len(line)):
            for j in range(len(classes)):
                try:
                    temp[j] += math.log10(classes[j][line[i]])
                except KeyError:
                    temp[j] += math.log10(classes[j]["UNK"])
        results.append(temp)
    return results


def save_list(results, output_file_addr):
    with open(output_file_addr, 'w', encoding="UTF-8") as output:
        for result in results:
            output.write(result + "\n")


def compute_evaluation_metrics(sys_results, truth):
    evaluations = {}
    # Accuracy
    count = 0
    for i in range(len(sys_results)):
        if sys_results[i] == truth[i]:
            count += 1
    evaluations["accuracy"] = count / len(sys_results)

    tp = 0
    fn = 0
    fp = 0
    for i in range(len(sys_results)):
        if truth[i] == 0:
            if sys_results[i] == 0:
                tp += 1
            else:
                fn += 1
    for i in range(len(truth)):
        if truth[i] == 1:
            if sys_results[i] == 0:
                fp += 1
    # Presicion
    evaluations["presicion"] = tp / (tp + fn)
    # Recall
    evaluations["recall"] = tp / (tp + fp)
    # F1
    f1 = 2 * (evaluations["presicion"] * evaluations["recall"]) / (evaluations["presicion"] + evaluations["recall"])
    evaluations["f1"] = f1
    return evaluations


def main(mode, data_address):
    if mode == "train":
        train_data = read_data_lines(data_address)
        global model
        model = train(train_data)
    if mode == "test":
        test_data = read_data_lines(data_address)
        results = test(test_data, model)
        temp = []
        for result in results:
            temp_line = ""
            for i in range(len(result)):
                temp_line += index_to_label[i] + " " + str(result[i]) + " "
            temp.append(temp_line)
        save_list(temp, output_addr)
        sys_results = [i.index(max(i)) for i in results]
        truth = [label_to_index[i[0]] for i in test_data]
        evaluations = compute_evaluation_metrics(sys_results, truth)
        temp = []
        for key in evaluations:
            temp.append(key + " = " + str(evaluations[key]))
        save_list(temp, eval_addr)

model = []
label_to_index = {}
index_to_label = {}

while True:
    mode = input()
    if mode == "train":
        label_to_index = {}
        index_to_label = {}
        model = []
        print("enter data address: ")
        address = input()
        main(mode, address)
        print("train is done.")
    if mode == "test":
        if len(model) != 0:
            print("enter output file name: (Test/TestCase)")
            data_type = input()
            eval_addr = eval.replace("{type}", data_type)
            output_addr = output.replace("{type}", data_type)
            print("enter data address: ")
            main(mode, input())
            print("test is done.")
        else:
            print("model is not trained.")
