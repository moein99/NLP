in this section, i gathered all words for label1 and label2 from Processed Transcripts in ProcessedData/label1 and ProcessedData/label2.
then i computed desired wordClouds and passed them to WordCloud library for visualization.

word cloud #1: words frequencies for label1
word cloud #2: words frequencies for label2
word cloud #5: words frequencies without stop words for label1
word cloud #6: words frequencies without stop words for label2
word cloud #3: label1 words frequencies minus label2 words frequencies. negative values are truncated to zero.
word cloud #4: label2 words frequencies minus label1 words frequencies. negative values are truncated to zero.
word cloud #7 and #8: same as 3 and 4 but stop words are removed. 

words_frequencies with and without stop words (word cloud # 1, 2, 5, 6): 
words frequencies without removing stop words show that which words are more frequent, so words like pronouns are more common than the others. but these words are usually common in every context and their presence is not going to help us for tasks like classification and generally finding a difference between labels. consequently, we delete them.

differential words_frequencies with and without stop words (word cloud #3, 4, 7, 8):
these word clouds highlight the difference between two labels. for a label, words that are common in it and uncommon in the other one have bigger font size . for the same reason in the above explanation, its better to remove stop words.


