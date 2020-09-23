import io
import csv
import os

DICT_NAME = "Entries.csv"
current_path = os.path.dirname(os.path.realpath(__file__))
dict_addr = os.path.abspath(os.path.join(current_path, "../in/" + DICT_NAME))

phon_to_written = {}
written_to_phon = {}
with io.open(dict_addr, 'r', encoding="UTF8") as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        phon_to_written[row[0]] = row[1]
        written_to_phon[row[1]] = row[0]
csvFile.close()

results = []

def calPossibleSequence(str, phon_to_written, prev_words):
    temp = ""
    length = len(str)
    for i in range(length):
        temp += str[i]
        if temp in phon_to_written:
            if i != length - 1:
                calPossibleSequence(str[i + 1:], phon_to_written ,prev_words + phon_to_written[temp] + " ")
            else:
                result = prev_words + phon_to_written[temp]
                results.append(result)

def saveResult(results, out_file_name):
    out_addr = "../out/" + out_file_name
    with open(out_addr, 'w', encoding="UTF8") as out:
        for result in results:
            out.write(result + "\n")


file_name = input()
file_addr = os.path.abspath(os.path.join(current_path, "../in/" + file_name))
with io.open(file_addr, 'r', encoding="UTF-8") as input_file:
    sentence = input_file.readline()
input_file.close()


phon_form = ""
for word in sentence.split():
    phon_form += written_to_phon[word]

calPossibleSequence(phon_form, phon_to_written, "")
saveResult(results, "out_" + file_name)