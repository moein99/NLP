from os import listdir
from os.path import join


label_data = "../../SplitData/{train_or_test}/label{label_num}/"
corpus_addr = "../corpus{label_num}_{train_test}.txt"

labels = ["1", "2"]
train_test = ["train", "test"]

for label_num in labels:
    for data_type in train_test:
        files_addr = label_data.replace("{train_or_test}", data_type).replace("{label_num}", label_num)
        for season in listdir(files_addr):
            season_addr = join(files_addr, season)
            for episode in listdir(season_addr):
                episode_addr = join(season_addr, episode)
                with open(episode_addr, 'r', encoding="UTF-8") as file:
                    lines = file.readlines()
                    corpus_file = corpus_addr.replace("{label_num}", label_num).replace("{train_test}", data_type)
                    with open(corpus_file, 'a', encoding="UTF-8") as corpus:
                        for line in lines:
                            corpus.write(line)
