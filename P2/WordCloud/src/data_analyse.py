from os import listdir
from os.path import join
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

label1_processedData_addr = "../../ProcessedData/label1/"
label2_processedData_addr = "../../ProcessedData/label2/"
stopwords_addr = "../stopwords.txt"
labels = [label1_processedData_addr, label2_processedData_addr]

stopwords = []
with open(stopwords_addr, 'r', encoding="UTF-8") as stopwords_file:
    lines = stopwords_file.readlines()
    for line in lines:
        stopwords.extend(line.split())

label1_words = []
label2_words = []
for label_data_addr in labels:
    all_label_words = []
    for season in listdir(label_data_addr):
        season_addr = join(label_data_addr, season)
        for episode in listdir(season_addr):
            episode_addr = join(season_addr, episode)
            with open(episode_addr, 'r', encoding="UTF-8") as episode_trans:
                lines = episode_trans.readlines()
                words = []
                for line in lines:
                    words.extend(line.split())
                all_label_words.extend(words)
    if label_data_addr == label1_processedData_addr:
        label1_words.extend(all_label_words)
    else:
        label2_words.extend(all_label_words)


label1_word_to_freq = dict(Counter(label1_words))
for key in label1_word_to_freq:
    label1_word_to_freq[key] /= len(label1_words)
print("label1 words frequencies calculated.")
label2_word_to_freq = dict(Counter(label2_words))
for key in label2_word_to_freq:
    label2_word_to_freq[key] /= len(label2_words)
print("label2 words frequencies calculated.")


label1_words_without_stopw = [i for i in label1_words if i not in stopwords]
label2_words_without_stopw = [i for i in label2_words if i not in stopwords]
label1_word_to_freq_stopw_rmvd = dict(Counter(label1_words_without_stopw))
for key in label1_word_to_freq_stopw_rmvd:
    label1_word_to_freq_stopw_rmvd[key] /= len(label1_words_without_stopw)
print("label1 words frequencies without stopwords calculated.")
label2_word_to_freq_stopw_rmvd = dict(Counter(label2_words_without_stopw))
for key in label2_word_to_freq_stopw_rmvd:
    label2_word_to_freq_stopw_rmvd[key] /= len(label2_words_without_stopw)
print("label2 words frequencies without stopwords calculated.")


label1_word_to_diff_freq = label1_word_to_freq.copy()
label2_word_to_diff_freq = label2_word_to_freq.copy()
label1_word_to_diff_freq_stopw_rmvd = label1_word_to_freq_stopw_rmvd.copy()
label2_word_to_diff_freq_stopw_rmvd = label2_word_to_freq_stopw_rmvd.copy()
for key in label1_word_to_diff_freq:
    if key in label2_word_to_diff_freq:
        val = label1_word_to_diff_freq[key] - label2_word_to_diff_freq[key]
        if val > 0:
            label1_word_to_diff_freq[key] = val
            label2_word_to_diff_freq[key] = 0
        else:
            label1_word_to_diff_freq[key] = 0
            label2_word_to_diff_freq[key] = -val
print("label1 & label2 differential words frequencies calculated.")
for key in label1_word_to_diff_freq_stopw_rmvd:
    if key in label2_word_to_diff_freq_stopw_rmvd:
        val = label1_word_to_diff_freq_stopw_rmvd[key] - label2_word_to_diff_freq_stopw_rmvd[key]
        if val > 0:
            label1_word_to_diff_freq_stopw_rmvd[key] = val
            label2_word_to_diff_freq_stopw_rmvd[key] = 0
        else:
            label1_word_to_diff_freq_stopw_rmvd[key] = 0
            label2_word_to_diff_freq_stopw_rmvd[key] = -val
print("label1 & label2 differential words frequencies without stopwords calculated.")

lst = [label1_word_to_freq, label2_word_to_freq, label1_word_to_diff_freq, label2_word_to_diff_freq, label1_word_to_freq_stopw_rmvd, label2_word_to_freq_stopw_rmvd, label1_word_to_diff_freq_stopw_rmvd, label2_word_to_diff_freq_stopw_rmvd]
for i in range(1, 9):
    word_cloud = WordCloud(width=1920, height=1080, max_words=5000, relative_scaling=1,
                           normalize_plurals=False).generate_from_frequencies(lst[i - 1])
    WordCloud.to_file(word_cloud, "../out/#.jpg".replace("#", str(i)))
    print("WordCloud# saved.".replace("#", str(i)))

# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()