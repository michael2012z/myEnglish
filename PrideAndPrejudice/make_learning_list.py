#!/usr/bin/python3
import os
import xml.etree.ElementTree as ET

def make_learning_list(level):
    print("handling word list level {}".format(level))
    # load Economist word list of a level
    buff = open("unknown_words_{}.txt".format(level), "rt").read()
    lines = buff.split("\n")
    words = []
    for line in lines:
        if len(line) > 0:
            words.append(line.split("\t")[0])

    # go through each word, load explanation, and write Markdown
    buff = []
    for word in words:
        d = load_word_def(word)
        explanation = format_explanation(d)
        buff.append("\n".join(explanation))
        print(".", end = "")
    fn = "learning-list-freq-{}.md".format(level)
    print("\ncreated {}".format(fn))
    open(fn, "wt").write("\n\n".join(buff))

    
def format_explanation(explanation):
    # explanation format: (word, pron, freq, defi, ety, family, examples, hints)
    text = []
    if explanation == None:
        return text
    # word
    if explanation[0] != None and len(explanation[0]) > 0:
        text.append("# " + explanation[0])
    # pron
    if explanation[1] != None and len(explanation[1]) > 0:
        text.append("**/" + explanation[1]+ "/**")
    # definition
    if explanation[3] != None and len(explanation[3]) > 0:
        text.append(explanation[3])
    # hints
    if explanation[7] != None and len(explanation[7]) > 0:
        text.append("### Definition")
        for hint in explanation[7]:
            text.append("- " + hint[0] + ": " + hint[1])
    # family
    if explanation[5] != None and len(explanation[5]) > 0:
        text.append("### Family")
        for f in explanation[5].split(";"):
            text.append("- " + f)
    # examples
    if explanation[6] != None and len(explanation[6]) > 0:
        text.append("### Examples")
        for example in explanation[6]:
            text.append("- " + example)
    # etymology
    if explanation[4] != None and len(explanation[4]) > 0:
        text.append("### Etymology")
        text.append(explanation[4])
    return text



def load_word_def(word):
    file_name = "../vocabulary/dictionary/dictionary/" + word[0].upper() + "/" + word + ".xml"
    if word[0].isalpha()== False or not os.path.exists(file_name):
        return None
        
    tree = ET.parse(file_name)
    word_data = tree.getroot()[0]
    word = ""
    pron = ""
    freq = 0
    defi = ""
    ety = ""
    family = ""
    examples = []
    hints = []
    for attr in word_data:
        if attr.tag == 'word':
            word = attr.text
        elif attr.tag == 'pron':
            pron = attr.text
        elif attr.tag == 'freq':
            freq = attr.text
        elif attr.tag == 'def':
            defi = attr.text
        elif attr.tag == 'family':
            family = attr.text
        elif attr.tag == 'examples':
            for example in attr:
                examples.append(example.text)
        elif attr.tag == 'hints':
            for hint in attr:
                p = ""
                m = ""
                for i in hint:
                    if i.tag == 'property':
                        p = i.text
                    else:
                        m = i.text
                hints.append((p, m))
    word_item = (word, pron, freq, defi, ety, family, examples, hints)
    return word_item


if __name__ == '__main__':
    make_learning_list(3)
    make_learning_list(2)
    
