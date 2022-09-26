# Использование:
1) Клонируйте репозиторий:
```git clone https://github.com/poli-nagibator/dict```
2) Установите зависимости для корректной работы скрипта
``` pip install -r requirements.txt```
3) Скачайте нужную книгу в формате ```.fb2``` в директорию со скриптом и запустите команду:
```sed -r '1,/<body>/d;/<\/body>/,$d;s/<[^>]+>//g;/^[[:space:]]*$/d' $(find . -iname *.fb2) | tee words.txt```
4) Запустите скрипт, он найдет нужные слова в книге:
```./parse.py```
5) Советую просмотреть список, некоторые слова убрать, некоторые добавить
6) Обратитесь ко мне за данными токена ;)
7) Запустите скрипт еще раз, он создаст таблицу
8)Лучше потом открыть таблицу и изменить название листа с "pyexcel_sheet1" на что-нибудь другое

Todo list:
- [ ] Change sheet name 
- [ ] Create random filenames
