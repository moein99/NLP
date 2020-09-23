from os import listdir
from os.path import join
from collections import Counter

label1_train_data_addr = "../../SplitData/train/label1/"
label2_train_data_addr = "../../SplitData/train/label2/"
test_data_addr = "../test/"
ngram_test_file = "in.#gram"
ngram_prob_test_file = "out.#gram.lm"
model1_ngram_probs_file = "label1.#gram.lm"
model2_ngram_probs_file = "label2.#gram.lm"


def ngrams(list_of_words, n):
    ng = []
    grams = [' '.join(list_of_words[i:i + n]) for i in range(len(list_of_words) - n + 1)]
    if n == 1:
        for gram in grams:
            ng.append(tuple([gram]))
    else:
        for gram in grams:
            if "</s>" in gram:
                if gram.count("</s>") > 1:
                    continue
                elif gram.split()[-1] != "</s>":
                    continue
            ng.append(tuple(gram.split()))
    return ng



def generate_ngram_prob(lines, n):
    list_of_words = []
    probs = {}
    for line in lines:
        list_of_words.extend(line.split())
    n_grams = [Counter(ngrams(list_of_words, 1))]
    n_grams[-1][tuple(["UNK"])] = 0
    for i in range(max(n - 1, 2), n + 1):
        n_grams.append(Counter(ngrams(list_of_words, i)))
        n_grams[-1][tuple(["UNK"] * i)] = 0
    vocab_length = len(n_grams[0]) - 2
    if n != 1:
        for key in n_grams[n - 1]:
            prev_ngram_key = tuple([key[j] for j in range(len(key) - 1)])
            probs[key] = (n_grams[n - 1][key] + 1) / (n_grams[n - 2][prev_ngram_key] + vocab_length)
    else:
        total_words = sum(n_grams[n - 1].values())
        for key in n_grams[n - 1]:
            probs[key] = (n_grams[n - 1][key] + 1) / (total_words + vocab_length)
    return probs


def get_label_lines(addr):
    lines = []
    for season in listdir(addr):
        season_addr = join(addr, season)
        for episode in listdir(season_addr):
            episode_addr = join(season_addr, episode)
            with open(episode_addr, 'r', encoding="UTF-8") as episode_trans:
                print(episode_addr)
                lines.extend(episode_trans.readlines())
    return lines


def get_test_data_lines(addr):
    lines = []
    with open(addr, 'r', encoding="UTF-8") as file:
        lines.extend(file.readlines())
    return lines


def get_test_probs(num_of_grams):
    test_lines = []
    probs = []
    for i in range(1, num_of_grams + 1):
        test_lines.append(get_test_data_lines(join(test_data_addr, ngram_test_file.replace("#", str(i)))))
    for i in range(len(test_lines)):
        probs.append((generate_ngram_prob(test_lines[i], i + 1), i + 1))
    return probs

def get_train_probs(label1_lines, label2_lines, num_of_grams):
    label1_probs = []
    label2_probs = []
    for i in range(1, num_of_grams + 1):
        label1_probs.append((generate_ngram_prob(label1_lines, i), i))
        label2_probs.append((generate_ngram_prob(label2_lines, i), i))
    return label1_probs, label2_probs


def save_ngrams_probs(list_of_probs, path, file_name):
    for prob, gram_number in list_of_probs:
        file_addr = join(path, file_name.replace("#", str(gram_number)))
        with open(file_addr, 'w', encoding="UTF-8") as file:
            for key in prob:
                tmp = ""
                for i in range(len(key)):
                    tmp += key[i] + '|'
                tmp += str(prob[key]) + "\n"
                file.write(tmp)


test_probs = get_test_probs(3)
save_ngrams_probs(test_probs, test_data_addr, ngram_prob_test_file)

label1_lines = get_label_lines(label1_train_data_addr)
label2_lines = get_label_lines(label2_train_data_addr)
label1_probs, label2_probs = get_train_probs(label1_lines, label2_lines, 3)
save_ngrams_probs(label1_probs, "../", model1_ngram_probs_file)
save_ngrams_probs(label2_probs, "../", model2_ngram_probs_file)

