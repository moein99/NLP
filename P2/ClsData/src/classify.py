from os import listdir
from os.path import join
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
label1_data_addr = "../../ProcessedData/label1/"
label2_data_addr = "../../ProcessedData/label2/"
train_data_addr = "../train.txt"
test_data_addr = "../test.txt"

data = [label1_data_addr, label2_data_addr]
dic = {0: 'joey', 1: "chandler", "train": train_data_addr, "test": test_data_addr}


def read_labels_paragraphs(labels_data_addr):
    label1_paragraphs = []
    label2_paragraphs = []
    labels = [label1_paragraphs, label2_paragraphs]
    label_index = 0
    for label_data_addr in labels_data_addr:
        for season in listdir(label_data_addr):
            season_addr = join(label_data_addr, season)
            for episode in listdir(season_addr):
                episode_addr = join(season_addr, episode)
                with open(episode_addr, 'r', encoding="UTF-8") as episode_trans:
                    print(episode_addr)
                    [labels[label_index].append([i for i in paragraph.split()[1: -2] if i not in stop_words]) for
                     paragraph in episode_trans.readlines()]
        label_index += 1
    return label1_paragraphs, label2_paragraphs


def split_data(data_lines, ratio):
    words_count = sum([len(i) for i in data_lines])
    train_paragraphs = []
    index = 0
    train_count = 0
    next_round_indices = []
    temp = data_lines.copy()
    while train_count / words_count < ratio:
        train_paragraphs.append(temp[index])
        train_count += len(temp[index])
        index += 2
        if index >= len(temp):
            if index == len(temp):
                next_round_indices.append(index - 1)
            index = 0
            temp = [temp[i] for i in next_round_indices]
            next_round_indices = []
        else:
            next_round_indices.append(index - 1)
    test_paragraphs = [temp[i] for i in next_round_indices] + temp[next_round_indices[-1] + 1:]
    return train_paragraphs, test_paragraphs


def save_data(data, type):
    addr = dic[type]
    with open(addr, 'w', encoding="UTF-8") as file:
        index = 0
        for label in data:
            for line in label:
                if len(line) > 0:
                    string = dic[index] + " "
                    for token in line:
                        string += token + " "
                    file.write(string + "\n")
            index += 1


label1_paragraphs, label2_paragraphs = read_labels_paragraphs(data)
train1, test1 = split_data(label1_paragraphs, 0.8)
train2, test2 = split_data(label2_paragraphs, 0.8)
save_data([train1, train2], "train")
save_data([test1, test2], "test")
