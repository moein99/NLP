from os import listdir
from os.path import join
from decimal import *

model_ngram_prob_file = "../../Model/label{model_num}.{gram_num}gram.lm"
label_data = "../../SplitData/{train_or_test}/label{model_label_num}/"


def read_model(model_addr):
    model = {}
    with open(model_addr, 'r', encoding="UTF-8") as file:
        lines = file.readlines()
        for line in lines:
            entry = line.split('|')
            model[tuple(entry[:len(entry) - 1])] = float(entry[-1])
    return model


def get_single_item_perp(item, root):
    item **= -1
    item **= 1 / root
    return Decimal(item)


def calculate_perplexity(text, model, num_of_grams):
    lines = text.split('\n')
    lines = lines[:len(lines) - 1]
    text_perplexity = Decimal(1)
    for line in lines:
        line = line.split()
        grams = [' '.join(line[i:i + num_of_grams]) for i in range(len(line) - num_of_grams + 1)]
        # line_perplexity = 0
        root = len(grams)
        for gram in grams:
            gram = tuple(gram.split())
            if gram in model:
                text_perplexity *= get_single_item_perp(model[gram], root)
            else:
                text_perplexity *= get_single_item_perp(model[tuple(["UNK"] * num_of_grams)], root)
                # line_perplexity = pow(10, line_perplexity)
                # inv_line_perp = Decimal(line_perplexity) ** -1
                # text_perplexity += math.log10(inv_line_perp ** Decimal(1 / len(grams)))
    return text_perplexity


def read_episode_scripts(label_num, train_or_test):
    scripts = []
    addr = label_data.replace("{train_or_test}", train_or_test).replace("{model_label_num}", str(label_num))
    for season in listdir(addr):
        season_addr = join(addr, season)
        for episode in listdir(season_addr):
            episode_addr = join(season_addr, episode)
            with open(episode_addr, 'r', encoding="UTF-8") as file:
                scripts.append(file.read())
    return scripts


def calculate_label_perplexity(label_scripts, model, num_of_grams):
    total_perplexity = 0
    for script in label_scripts:
        total_perplexity += calculate_perplexity(script, model, num_of_grams)
    return total_perplexity


label1_train_scripts = read_episode_scripts(1, "train")
label1_test_scripts = read_episode_scripts(1, "test")
label2_train_scripts = read_episode_scripts(2, "train")
label2_test_scripts = read_episode_scripts(2, "test")

models = {}
for model_label_num in ["1", "2"]:
    for gram_num in [1, 2, 3]:
        models[(model_label_num, gram_num)] = read_model(
            model_ngram_prob_file.replace("{model_num}", model_label_num).replace("{gram_num}", str(gram_num)))

results = {}
for key in models:
    model_label_num, gram_num = key
    model = models[key]
    results[(model_label_num, "1", "train", gram_num)] = calculate_label_perplexity(label1_train_scripts, model, gram_num)
    results[(model_label_num, "1", "test", gram_num)] = calculate_label_perplexity(label1_test_scripts, model, gram_num)
    results[(model_label_num, "2", "train", gram_num)] = calculate_label_perplexity(label2_train_scripts, model, gram_num)
    results[(model_label_num, "2", "test", gram_num)] = calculate_label_perplexity(label2_test_scripts, model, gram_num)

data_string = "data = label{label} {data_type} data"
model_string = "model = label{label} {gram}gram"
perp_string = "perplexity: {perp}"
dic = {1: "uni", 2: "bi", 3: "tri"}
for result in results:
    model_label_num, data_num, data_type, gram = result
    print(model_string.replace("{label}", model_label_num).replace("{gram}", dic[gram]))
    print(data_string.replace("{label}", data_num).replace("{data_type}", data_type))
    print(perp_string.replace("{perp}", str(results[result])))
    print("-" * 20)
