#!/usr/bin/python3

import os
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer

def get_file_word_list(file_name):
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
    current_folder = ""
    for root, dirs, files in os.walk("./pages"):
    # for root, dirs, files in os.walk("./test_pages"):
        for f in files:
            if root != current_folder:
                current_folder = root
                print("handling folder {}".format(current_folder))
            file_path = os.path.join(root, f)
            file_words = get_file_word_list(file_path)
            for word_count_tuple in file_words.items():
                if not word_count_tuple[0] in word_count:
                    word_count[word_count_tuple[0]] = 0
                word_count[word_count_tuple[0]] += word_count_tuple[1]
            
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    # load word frequency data
    freqs = []
    for i in range(5):
        freqs.append(set(open("../frequency/words-"+str(i+1)+".txt", "rt").read().split('\n')))

    f = []
    for i in range(5):
        f.append(open("word_count-" + str(i+1) + ".txt", "wt"))

    f_unknown = open("word_count-0.txt", "wt")

    num_all_words = 0
    num_freq_words = 0
    for word in sorted_word_count:
        num_all_words += word[1]
        for i in range(5):
            freq = freqs[i]
            if len(word[0]) < 20 and word[0] in freq:
                f[i].write("{}\t\t\t{}\n".format(word[0], word[1]))
                num_freq_words += word[1]
                break
        else:
            f_unknown.write("{}\t\t\t{}\n".format(word[0], word[1]))

    for i in range(5):
        f[i].close()
    f_unknown.close()
    
    print("{} words handled, {} words categorised.".format(num_all_words, num_freq_words))
    
