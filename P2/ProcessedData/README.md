i normalized and tokenized each episode transcript in Data/label1 and Data/label2 directory and save it to ProcessedData/label1 and ProcessedData/label2.

in normalization i did the following steps for each line:
1- converting all letters to lower case
2- removing numbers
3- removing punctuations
4- removing white spaces

after normalization step, i tokenized the line using nltk library in python then word tokens are stored in ProcessedData/label1 and ProcessedData/label2.