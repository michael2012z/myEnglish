from bs4 import BeautifulSoup

html_doc =  open('pages/2020-03-21/Closed by covid-19 - Paying to stop the pandemic _ Leaders _ The Economist.html', "rt").read()

soup = BeautifulSoup(html_doc, 'html.parser')


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
        if c.isalpha() and alpha_begin == -1:
            alpha_begin = i
        if c.isalpha() == False and alpha_begin != -1:
            alpha_end = i
            break
        i += 1
    print(word)
    print(word[alpha_begin: alpha_end])
            

