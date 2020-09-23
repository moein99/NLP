train_data_addr = "../../../ClsData/train.txt"
test_data_addr = "../../../ClsData/test.txt"
train_data_output_addr = "../input.train.txt"
test_data_output_addr = "../input.test.txt"
label_to_index = {}
index_to_label = {}


def read_data_lines(addr):
    with open(addr, 'r', encoding="UTF-8") as file:
        return [i.split() for i in file.readlines()]


def get_ngram(data, n):
    ngrams = []
    for line in data:
        ngrams.append({})
        for i in range(len(line) - n + 1):
            temp = ' '.join(line[i:i + n])
            temp = '-'.join(temp.split())
            if temp in ngrams[-1]:
                ngrams[-1][temp] += 1
            else:
                ngrams[-1][temp] = 1
    return ngrams


def get_ngrams_feature(data):
    features = []
    unigram = get_ngram(data, 1)
    bigram = get_ngram(data, 2)
    trigram = get_ngram(data, 3)
    ngrams_names = {1: 'uni_', 2: 'bi_', 3: 'tri_'}
    ngrams = [unigram, bigram, trigram]
    for i in range(len(data)):
        string = ""
        for j in range(len(ngrams)):
            string += ' '.join(
                ngrams_names[j + 1] + str(key) + ':' + str(val) for key, val in ngrams[j][i].items()) + ' '
        features.append(string)
    return features


def get_sentence_length_feature(data):
    features = []
    for line in data:
        features.append("len:" + str(len(line)))
    return features


def generate_features(train_data):
    input_data = []
    labels = [line[0] for line in train_data]
    data = [line[1:] for line in train_data]
    features = []
    ngrams_feature = get_ngrams_feature(data)
    features.append(ngrams_feature)
    length_feature = get_sentence_length_feature(data)
    features.append(length_feature)
    for i in range(len(labels)):
        string = labels[i] + ' '
        for feature in features:
            string += feature[i]
        input_data.append(string)
    return input_data


def save_list(lines, output_file_addr):
    with open(output_file_addr, 'w', encoding="UTF-8") as output:
        for line in lines:
            output.write(line + "\n")


train_data = read_data_lines(train_data_addr)
test_data = read_data_lines(test_data_addr)
input_data = generate_features(train_data)
save_list(input_data, train_data_output_addr)
input_data = generate_features(test_data)
save_list(input_data, test_data_output_addr)