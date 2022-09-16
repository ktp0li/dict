import requests
from bs4 import BeautifulSoup
import string
import time
words = set(open('words.txt').read().lower().translate(str.maketrans('', '', string.punctuation)).replace('“','').replace('”','').replace('’','').replace('‘', '').split())
used_words = []
for word in words:
    try:
        new_words = set(open('new_words.txt').read().split())
    except FileNotFoundError:
        new_words = []

    if word in new_words:
        continue
    else:
        url = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + word
        r = requests.get(url, allow_redirects=True,headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})

        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            level = soup.ol.li.span.span.get('class')[0]
            if level == 'ox5ksym_c1':
                print(word, level)
                open('new_words.txt', 'a').write(word + '\n')
            else: 
                used_words.append(word)
        except AttributeError:
            print(f'no such word "{word}"')
            used_words.append(word)
