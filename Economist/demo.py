from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer

html_doc =  open('pages/2020-03-21/Closed by covid-19 - Paying to stop the pandemic _ Leaders _ The Economist.html', "rt").read()

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
    
    #for i in range(len(word), 0, -1):
    #    if word[i-1].isalpha():
    #        break
    #alpha_end = i

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

word_freq_list = sorted(word_freq.items(), key=lambda x: x[1])
for word in word_freq_list:
    print(word)

