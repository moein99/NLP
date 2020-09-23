from os import listdir
from os import makedirs
from os.path import join

FIRST_PERSON = "joey"
SECOND_PERSON = "chandler"

trans_addr = "../../RawData/Transcripts"
label1_addr = "../label1/"
label2_addr = "../label2/"


def save_dialogues(dialogues, season_num, episode_name, person):
    if person == FIRST_PERSON:
        file_directory = join(label1_addr, season_num)
    else:
        file_directory = join(label2_addr, season_num)
    try:
        makedirs(file_directory)
    except FileExistsError:
        pass

    with open(join(file_directory, episode_name), 'w', encoding="UTF-8") as file:
        for dialogue in dialogues:
            file.write(dialogue)

for season in listdir(trans_addr):
    season_addr = join(trans_addr, season)
    for episode in listdir(season_addr):
        episode_addr = join(season_addr, episode)
        with open(episode_addr, 'r', encoding="UTF-8") as episode_trans:
            print(season)
            print(episode)
            lines = episode_trans.readlines()
            first_person_dialogues = []
            second_person_dialogues = []
            for line in lines:
                if ':' in line:
                    speakers = line[:line.index(":")].lower()
                    text = line[line.index(":") + 2:]
                    if FIRST_PERSON in speakers:
                        first_person_dialogues.append(text)
                    if SECOND_PERSON in speakers:
                        second_person_dialogues.append(text)
        save_dialogues(first_person_dialogues, season, episode, FIRST_PERSON)
        save_dialogues(second_person_dialogues, season, episode, SECOND_PERSON)