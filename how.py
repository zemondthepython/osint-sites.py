# Імпортувати необхідні бібліотеки
import requests
import sys 
import os 
import urllib.request 
import string 

# Визначаємо поточний каталог
currentDir = os.getcwd()

# Встановлюємо ліміт об’єктів 
limit = 10

# Функція для виконання запиту 
def run_query(query):
    # задаємо адресу, яку ми запитуємо 
    request = requests.get("http://api.hackertarget.com/geoip/?q=" + query) 

    # повертаємо відповідь на запит 
    if request.status_code == 200: 
        return request.content 
    else: 
        raise Exception("Невірний запит")

# Функція для збереження URL в файл 
def log_urls(urls): 
    # Встановити ліміт на кількість завантажених файлів
    i = 0
    for url in urls: 
        if i > limit: 
            break 
        # Завантажити дані 
        content = urllib.request.urlopen(url).read() 
        print("[+] Downloading file: " + str(url)) 
        # Зберегти дані
        name = url.split('/')[-1] 
        fileName = currentDir + '/' + name 
        with open(fileName, 'wb') as f: 
            f.write(content) 
            i += 1

# Отримати список сайтів які потрібно викачати
def get_urls(): 
    with open ('url_list.txt','r') as f: 
        return f.readlines() 

# Функція для сканування сайтів
def scan_sites(): 
    # Отримати IP-адреси з вхідного файлу 
    url_list = get_urls() 
    print("[+] IP-list: " + str(url_list))

    # Отримати та зберегти всю інформацію про ці сайти у файл 
    for url in url_list:
        print("[+] Scanning site: " + str(url)) 
        # Виконати запит 
        response = run_query(url) 
        # Зберегти результати до текстового файлу
        fileName = currentDir + '/' + url + '.txt' 
        with open(fileName, 'w') as f: 
            f.write(response.decode('utf-8'))

# Запуск процесу
if __name__ == "__main__": 
    scan_sites() 
    log_urls(get_urls())