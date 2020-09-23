from os import listdir
from os import makedirs
from os.path import join
from nltk.tokenize import word_tokenize
import re
import string

label1_data_addr = "../../Data/label1/"
label2_data_addr = "../../Data/label2/"
data = [label1_data_addr, label2_data_addr]

label1_processedData_addr = "../label1/"
label2_processedData_addr = "../label2/"


def normalize(input_str):
    input_str = input_str.lower()
    input_str = re.sub("r’\d+’", '', input_str)
    input_str = input_str.translate(str.maketrans('', '', string.punctuation + u'\x92'))
    input_str = input_str.strip()
    return input_str

def save_processed_data(dialogues_words, season, episode_name, label):
    if label == label1_data_addr:
        file_directory = join(label1_processedData_addr, season)
    else:
        file_directory = join(label2_processedData_addr, season)
    try:
        makedirs(file_directory)
    except FileExistsError:
        pass

    with open(join(file_directory, episode_name), 'w', encoding="UTF-8") as file:
        for dialogue in dialogues_words:
            file.write("<s> ")
            for word in dialogue:
                file.write(word + " ")
            file.write("</s>\n")

for label_data_addr in data:
    for season in listdir(label_data_addr):
        season_addr = join(label_data_addr, season)
        for episode in listdir(season_addr):
            episode_addr = join(season_addr, episode)
            with open(episode_addr, 'r', encoding="UTF-8") as episode_trans:
                print(episode_addr)
                dialogues = episode_trans.readlines()
                dialogues_words = []
                for dialogue in dialogues:
                    line = normalize(dialogue)
                    dialogues_words.append(word_tokenize(line))
            save_processed_data(dialogues_words, season, episode, label_data_addr)
