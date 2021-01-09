#!/usr/bin/python3

import os
import sys
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer

def search_in_file(word_to_search, txt_path):
    wordnet_lemmatizer = WordNetLemmatizer()
    found_lines = []
    all_text = ""
    with open(txt_path, "r") as txt_file:
        all_text = txt_file.read()
    lines = all_text.split(".")

    for line in lines:
        line = line.lstrip() + "."
        words = line.split()
        for word in words:
            if nltk.pos_tag([word])[0][1][0] == 'V':
                word = wordnet_lemmatizer.lemmatize(word, 'v')
            else:
                word = wordnet_lemmatizer.lemmatize(word)
            if word == word_to_search and (not (line in found_lines)):
                found_lines.append(line)

    return found_lines


if __name__ == '__main__':
    # para 1: word
    # para 2: folder
    word_to_search = ""
    folder_to_search = ""
    if len(sys.argv) > 1:
        word_to_search = sys.argv[1]
    if len(sys.argv) > 2:
        folder_to_search = sys.argv[2]

    pages_root = "./pages"
    for root, dirs, files in os.walk(pages_root):
        for f in files:
            if folder_to_search == "" or folder_to_search == root.split("/")[-1]:
                if f.split(".")[-1] == "txt":
                    found_lines = search_in_file(word_to_search, root + "/" + f)
                    if len(found_lines) > 0:
                        print("{}/{}:".format(root, f))
                        for line in found_lines:
                            print(" - {}".format(line))
