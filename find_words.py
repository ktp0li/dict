#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from fake_user_agent import user_agent
from os import path
from re import sub

path = path.dirname(path.realpath(__file__))
url = 'https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000'
request = requests.session().get(url, headers={'User-Agent': user_agent()})
words = set(sub('[“”’‘0-9,.:;–()!?-]', '', open(path + '/words.txt')
            .read().lower()).split())
wordlist = []

soup = BeautifulSoup(request.text, 'html.parser')
records = soup.find(id="wordlistsContentPanel").find_all('li')
for record in records:
    if record.get('data-ox5000') == 'c1':
        wordlist.append(record.get('data-hw'))

for word in words:
    try:
        new_words = set(open(path + '/new_words.txt').read().split())
    except FileNotFoundError:
        new_words = []

    if word in new_words:
        continue
    else:
        if word in wordlist:
            print(f'найдено слово \'{word}\'')
            open(path + '/new_words.txt', 'a').write(word + '\n')
