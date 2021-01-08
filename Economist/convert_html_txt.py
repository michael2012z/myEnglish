#!/usr/bin/python3

import os
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer

def get_html_text(file_name):
    html_doc =  open(file_name, "rt").read()
    wordnet_lemmatizer = WordNetLemmatizer()
    soup = BeautifulSoup(html_doc, 'html.parser')

    text = ''
    divs = soup.find_all('div')
    for div in divs:
        if "itemprop" in div.attrs and div.attrs["itemprop"] == "text":
            text += div.get_text()

    return text
    
    
if __name__ == '__main__':
    word_count = dict()
    file_list = []
    issues = 0
    current_folder = ""
    for root, dirs, files in os.walk("./pages"):
    # for root, dirs, files in os.walk("./test_pages"):
        for f in files:
            if root != current_folder:
                issues += 1
                current_folder = root
                print("handling folder {}".format(current_folder))
            html_path = os.path.join(root, f)
            text = get_html_text(html_path)
            text = text.split('■')[0]
            txt_path = html_path[:-4] + "txt"
            with open(txt_path, "w") as txt_file:
                txt_file.write(text)
            
