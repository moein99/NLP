model = label1 unigram
data = label2 train data
perplexity: 6.690699533616929460639747604E+284
--------------------
model = label2 trigram
data = label1 train data
perplexity: 1.610795409011290000841171757E+327
--------------------
model = label2 bigram
data = label2 train data
perplexity: 1.018022971185741115761118486E+336
--------------------
model = label2 bigram
data = label1 test data
perplexity: 7.209851741992745692583956823E+207
--------------------
model = label2 unigram
data = label2 train data
perplexity: 2.441179200718610797348441722E+280
--------------------
model = label1 bigram
data = label1 train data
perplexity: 8.285467968068655362729208550E+256
--------------------
model = label2 bigram
data = label1 train data
perplexity: 3.729266729734142755949795400E+278
--------------------
model = label2 unigram
data = label1 train data
perplexity: 1.645003984766845955092429609E+230
--------------------
model = label2 trigram
data = label2 test data
perplexity: 8.108996813970336287473147572E+292
--------------------
model = label1 bigram
data = label2 test data
perplexity: 5.972017125393194027883955029E+245
--------------------
model = label2 bigram
data = label2 test data
perplexity: 3.551603761707644401645369845E+247
--------------------
model = label1 unigram
data = label2 test data
perplexity: 9.375680255161489193496055228E+199
--------------------
model = label1 trigram
data = label1 test data
perplexity: 3.753025006637128741752629924E+238
--------------------
model = label2 trigram
data = label1 test data
perplexity: 5.902747695281720320184339249E+240
--------------------
model = label2 trigram
data = label2 train data
perplexity: 9.718302255259867337124593534E+380
--------------------
model = label2 unigram
data = label2 test data
perplexity: 3.645567718029872384046159529E+199
--------------------
model = label2 unigram
data = label1 test data
perplexity: 3.900349905586168071250832296E+168
--------------------
model = label1 unigram
data = label1 test data
perplexity: 3.052249295631933065116281316E+167
--------------------
model = label1 bigram
data = label1 test data
perplexity: 3.192863973426438355359925521E+205
--------------------
model = label1 trigram
data = label2 test data
perplexity: 3.112491679037225449011381349E+291
--------------------
model = label1 unigram
data = label1 train data
perplexity: 3.226910849943135209148556057E+224
--------------------
model = label1 bigram
data = label2 train data
perplexity: 1.177644715626005742714474277E+351
--------------------
model = label1 trigram
data = label2 train data
perplexity: 1.112229163534916606285705311E+410
--------------------
model = label1 trigram
data = label1 train data
perplexity: 3.583105541704660961791084010E+294
--------------------



conclusion:
generally, test data perplexity is lower compared to train data because there are fewer tokens in test data.
as we increase the number of grams, perplexity also increases. we know that perplexity is weighted equivalent branching factor.
in unigrams, there are |V| possible choices but this amount can increase up to |V|^2 in bigrams and also |V|^3 in trigrams. we observe that the branching factor is increasing here.
when a trained model is used on another label (train or test) it results higher perplexity compare to same label that the model was trained on. the reason is that when we use a model on different dataset, the UNK token will appear and it has the lowest probability. lower probability causes higher perplexity. it reminds us that perplexity is weighted equivalent branching factor. 

for example label1 trigram on label1 test data will result perplexity of 3.8E+238 but it results perplexity of 3.2E+291 on label2 test data because UNK tokens are more likely to happen in label2 that label1.
