from os import listdir
from os import makedirs
from os.path import join

label1_data_addr = "../../ProcessedData/label1/"
label2_data_addr = "../../ProcessedData/label2/"
label1_splited_addr = "../###/label1"
label2_splited_addr = "../###/label2"
splited_data = [label1_splited_addr, label2_splited_addr]
data = [label1_data_addr, label2_data_addr]


class Episode:
    def __init__(self, season, episode_name, word_count, label, dialogues):
        self.season = season
        self.episode_name = episode_name
        self.word_count = word_count
        self.label = label
        self.lines = dialogues


def get_labels_word_count(data_addr):
    label1_episode_to_word_count = []
    label2_episode_to_word_count = []
    labels = [label1_episode_to_word_count, label2_episode_to_word_count]
    label_index = 0
    for label_data_addr in data_addr:
        for season in listdir(label_data_addr):
            season_addr = join(label_data_addr, season)
            for episode in listdir(season_addr):
                episode_addr = join(season_addr, episode)
                with open(episode_addr, 'r', encoding="UTF-8") as episode_trans:
                    print(episode_addr)
                    dialogues = episode_trans.readlines()
                    word_count = 0
                    for dialogue in dialogues:
                        word_count += len(dialogue.split())
                    labels[label_index].append(Episode(season, episode, word_count, label_index, dialogues))
        label_index += 1
    return labels


def get_train_test_data_episodes(labels_word_count):
    train_episodes = []
    for label in labels_word_count:
        total_words = 0
        total_words_for_train = 0
        label_train_episodes = []
        for episode in label:
            total_words += episode.word_count
        index = 0
        next_round_indices = []
        temp_label = label.copy()
        while total_words_for_train / total_words < 0.8:
            episode = temp_label[index]
            total_words_for_train += episode.word_count
            label_train_episodes.append(episode)
            index += 2
            if index >= len(temp_label):
                index = 0
                temp_label = [temp_label[i] for i in next_round_indices]
                next_round_indices = []
            else:
                next_round_indices.append(index - 1)
        temp_label = [temp_label[i] for i in next_round_indices] + temp_label[next_round_indices[-1] + 1:]
        print(total_words_for_train / total_words)
        train_episodes.append((label_train_episodes, temp_label))
    return train_episodes


def save_train_test_data(train_test_data_episodes, splited_data):
    for train, test in train_test_data_episodes:
        lst = [(train, "train"), (test, "test")]
        for data_type, type in lst:
            for episode in data_type:
                if episode.label == 0:
                    file_directory = join(splited_data[0].replace("###", type), episode.season)
                else:
                    file_directory = join(splited_data[1].replace("###", type), episode.season)
                try:
                    makedirs(file_directory)
                except FileExistsError:
                    pass
                save_data(file_directory, episode.episode_name, episode.lines)


def save_data(path, file_name, data):
    with open(join(path, file_name), 'w', encoding="UTF-8") as file:
        for item in data:
            file.write(item)
        file.close()


labels_word_count = get_labels_word_count(data)
train_test_data_episodes = get_train_test_data_episodes(labels_word_count)
save_train_test_data(train_test_data_episodes, splited_data)
