#!/usr/bin/python3

import os
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer

def get_file_word_list(file_name):
    print("handling {}".format(file_name))
    html_doc =  open(file_name, "rt").read()
    wordnet_lemmatizer = WordNetLemmatizer()
    soup = BeautifulSoup(html_doc, 'html.parser')
    words = []

    text = ''
    divs = soup.find_all('div')
    for div in divs:
        if "itemprop" in div.attrs and div.attrs["itemprop"] == "text":
            text += div.get_text()

    for word in text.split():
        alpha_begin = -1
        alpha_end = len(word)
        i = 0
        for c in word:
            if word[i].isalpha():
                break
            else:
                i += 1
        alpha_begin = i

        for c in word[alpha_begin:]:
            if word[i].isalpha() == False:
                break
            else:
                i += 1
        alpha_end = i
    
        if alpha_end > alpha_begin:
            word = word[alpha_begin: alpha_end].lower()
            if nltk.pos_tag([word])[0][1][0] == 'V':
                word = wordnet_lemmatizer.lemmatize(word, 'v')
            else:
                word = wordnet_lemmatizer.lemmatize(word)
            words.append(word)

    print("{} words counted".format(len(words)))

    word_freq = dict()
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    return word_freq
    
    
if __name__ == '__main__':
    word_count = dict()
    file_list = []
    for root, dirs, files in os.walk("./pages"):
        for f in files:
            file_list.append(os.path.join(root, f))
    for file_path in file_list:
        file_words = get_file_word_list(file_path)
        for word_count_tuple in file_words.items():
            if not word_count_tuple[0] in word_count:
                word_count[word_count_tuple[0]] = 0
            word_count[word_count_tuple[0]] += word_count_tuple[1]

            
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1])

    # load word frequency data
    for i in range(5):
        freq = set(open("../frequency/words-"+str(i+1)+".txt", "rt").read().split('\n'))
        print(freq)
        f = open("word_count-" + str(i+1) + ".txt", "wt")
        for word in sorted_word_count:
            if len(word[0]) < 20 and word[0] in freq:
                f.write("{}\t\t\t{}\n".format(word[0], word[1]))
        f.close()
    
            
    
    
