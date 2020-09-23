import random

model_ngram_prob_file = "../../Model/label{model_num}.{gram_num}gram.lm"
saving_addr = "../label{label_num}.{gram_num}gram.gen"
CONST = 10 ** 9 + 7


def read_model(model_addr, gram_num):
    model = {}
    with open(model_addr, 'r', encoding="UTF-8") as file:
        lines = file.readlines()
        for line in lines:
            entry = line.split('|')
            seq_of_tokens = entry[:len(entry) - 1]
            value = float(entry[-1])
            for i in range(gram_num):
                tmp = model
                for j in range(i):
                    tmp = tmp[seq_of_tokens[j]]
                if seq_of_tokens[i] not in tmp:
                    if i == gram_num - 1:
                        tmp[seq_of_tokens[i]] = value
                    else:
                        tmp[seq_of_tokens[i]] = {}
    return model


def gen_text(model, gram_num, seeds, n):
    sentences = []
    if gram_num == 1:
        UNI_GRAM_LIMIT = 10
        s_val = 0
        s_val = model["<s>"]
        del model["<s>"]
        for i in range(n):
            sentence = "<s> "
            last_gram = ""
            count = 1
            while last_gram != "</s>":
                random.seed(seeds[i] * UNI_GRAM_LIMIT + count)
                count += 1
                last_gram = random.choice(sorted(list(model.keys())))
                if last_gram == "<s>":
                    continue
                else:
                    sentence += last_gram + " "
                    if len(sentence.split()) == UNI_GRAM_LIMIT - 1:
                        last_gram = "</s>"
                        sentence += last_gram
            sentences.append(sentence)
        model["<s>"] = s_val
    else:
        for i in range(n):
            sentence = "<s> "
            tmp_dic = model["<s>"]
            for j in range(gram_num - 1):
                random.seed(seeds[i])
                seeds[i] = (seeds[i] ** 2 + 1) % CONST
                tmp_str = random.choice(sorted(list(tmp_dic.keys())))
                sentence += tmp_str + " "
                tmp_dic = tmp_dic[tmp_str]
            prev_tokens = sentence.split()[1:]
            while prev_tokens[-1] != "</s>":
                tmp_dic = model
                for token in prev_tokens:
                    tmp_dic = tmp_dic[token]
                random.seed(seeds[i])
                seeds[i] = (seeds[i] ** 2 + 1) % CONST
                tmp_str = random.choice(sorted(list(tmp_dic.keys())))
                sentence += tmp_str + " "
                del prev_tokens[0]
                prev_tokens.append(tmp_str)
            sentences.append(sentence)
    return sentences


def save_results(results):
    for label_num, gram_num in results:
        addr = saving_addr.replace("{label_num}", label_num).replace("{gram_num}", str(gram_num))
        with open(addr, 'w', encoding="UTF-8") as file:
            for sentence in results[(label_num, gram_num)]:
                file.write(sentence + "\n")


models = {}
seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
number_of_sentences = 10
results = {}

for label_num in ["1", "2"]:
    for gram_num in [1, 2, 3]:
        models[(label_num, gram_num)] = read_model(
            model_ngram_prob_file.replace("{model_num}", label_num).replace("{gram_num}", str(gram_num)), gram_num)
        results[(label_num, gram_num)] = gen_text(models[(label_num, gram_num)], gram_num, seeds, number_of_sentences)
save_results(results)
