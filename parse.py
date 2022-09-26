#!/usr/bin/env python
from os import path
from requests import get, session
from json import loads
from pyexcel import get_sheet, save_as
from configparser import ConfigParser
from re import sub
from fake_user_agent import user_agent
from bs4 import BeautifulSoup

path = path.dirname(path.realpath(__file__))


def spelling(dictionary):
    try:
        return('[' + dictionary['results'][0]['lexicalEntries'][0]['entries']
               [0]['pronunciations'][0]['phoneticSpelling'] + ']')
    except KeyError:
        return 'ERROR'


def meaning(dictionary):
    try:
        return(dictionary['results'][0]['lexicalEntries'][0]['entries']
               [0]['senses'][0]['definitions'][0])
    except KeyError:
        try:
            return(dictionary['results'][0]['lexicalEntries'][0]['entries']
                   [0]['senses'][0]['subsenses'][0]['definitions'][0])
        except KeyError:
            return 'ERROR'


def translation(word_id, app_id, app_key):
    url = 'https://od-api.oxforddictionaries.com/api/v2/translations/en/ru/'\
            + word_id.lower() + '?strictMatch=false&fields=translations'
    request = get(url, headers={'app_id': app_id, 'app_key': app_key})
    dictionary = loads(request.text)
    try:
        return(dictionary['results'][0]['lexicalEntries'][0]['entries']
               [0]['senses'][0]['translations'][0]['text'])
    except KeyError:
        return 'ERROR'


def sentence(word_id, app_id, app_key):
    url = 'https://od-api.oxforddictionaries.com/api/v2/sentences/en/'\
            + word_id.lower() + '?strictMatch=false'
    request = get(url, headers={'app_id': app_id, 'app_key': app_key})
    dictionary = loads(request.text)
    try:
        return(dictionary['results'][0]['lexicalEntries']
               [0]['sentences'][0]['text'])
    except KeyError:
        return 'ERROR'


def parse():
    config = ConfigParser()
    config.read(path + "/api.txt")
    app_id = config.get("api", "app_id")
    app_key = config.get("api", "app_key")
    sheet_name = path + '/export.xls'
    words = set(open(path + '/new_words.txt').read().lower().split())

    try:
        sheet = get_sheet(file_name=sheet_name)
    except FileNotFoundError:
        save_as(array=[['слово', 'транскрипция', 'перевод', 'значение',
                       'предложение']], dest_file_name=sheet_name)
    sheet = get_sheet(file_name=sheet_name)

    for word_id in words:
        url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/en-gb'\
                + '/' + word_id.lower() + '?strictMatch=false'
        request = get(url, headers={'app_id': app_id, 'app_key': app_key})
        dictionary = loads(request.text)
        row = [word_id, spelling(dictionary), translation
               (word_id, app_id, app_key), meaning(dictionary),
               sentence(word_id, app_id, app_key)]
        sheet.row += row
        sheet.save_as(sheet_name)
        print(row)


def find():
    url = 'https://www.oxfordlearnersdictionaries.com/wordlists/'\
            + 'oxford3000-5000'
    request = session().get(url, headers={'User-Agent': user_agent()})
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


try:
    wordcount = len(open(path + '/new_words.txt').read().split())
except FileNotFoundError:
    wordcount = 0

print(f'Найдено {wordcount} слов.')
if wordcount != 0:
    print('Создание таблицы...')
    parse()
else:
    print('Поиск С1 слов в книге...')
    find()
    print('Советую открыть файл new_words.txt, просмотреть \
его содержимое, удалить неподходящие слова и вписать нужные')
