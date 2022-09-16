import requests
import json
import pyexcel

app_id = ''
app_key = ''
sheet_name = 'export.xls'
words = set(open('new_words.txt').read().lower().split())
try:
    sheet = pyexcel.get_sheet(file_name=sheet_name)
except FileNotFoundError:
    pyexcel.save_as(array=[['слово', 'транскрипция', 'перевод', 'значение', 'предложение']], dest_file_name=sheet_name)
    sheet = pyexcel.get_sheet(file_name=sheet_name)

def spelling():
    try:
        return '[' + dictionary['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['phoneticSpelling'] + ']'
    except KeyError:
        return 'ERROR'

def meaning():
    try:
        return dictionary['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    except KeyError:
        try:
            return dictionary['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['subsenses'][0]['definitions'][0]
        except KeyError:
            return 'ERROR'

def translation():
    url = 'https://od-api.oxforddictionaries.com/api/v2/translations/en/ru/' + word_id.lower() + '?strictMatch=false&fields=translations'
    request = requests.get(url, headers = {'app_id': app_id, 'app_key' : app_key})
    dictionary = json.loads(request.text)
    try:
        return dictionary['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['translations'][0]['text']
    except KeyError:
        return 'ERROR'

def sentence():
    url = 'https://od-api.oxforddictionaries.com/api/v2/sentences/en/' + word_id.lower() + '?strictMatch=false'
    request = requests.get(url, headers = {'app_id': app_id, 'app_key' : app_key})
    dictionary = json.loads(request.text)
    try:
        return dictionary['results'][0]['lexicalEntries'][0]['sentences'][0]['text']
    except KeyError:
        return 'ERROR'

for word_id in words:
    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/en-gb/' + word_id.lower() + '?strictMatch=false'
    request = requests.get(url, headers = {'app_id': app_id, 'app_key' : app_key})
    dictionary = json.loads(request.text)
    row = [word_id, spelling(), translation(), meaning(), sentence()]
    sheet.row += row
    sheet.save_as(sheet_name)
    print(row)
  


