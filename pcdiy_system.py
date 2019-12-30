from bs4 import BeautifulSoup
import requests
import time
import re

coolpcData = {}


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def wash(raw):
    left = raw.rfind('$')
    left2 = raw.find('$')
    right = raw.rfind(' ')
    money = raw[left:right].replace('◆', '').replace('★', '').replace('熱賣', '').strip()
    product = raw[:left2 - 2]
    coolpcData[product] = money
    return product


def coolpc():

    r = requests.get('http://www.coolpc.com.tw/evaluate.php')  # 爬取網頁內容
    if r.status_code == requests.codes.ok:  # 確認網頁狀態
        soup = BeautifulSoup(r.text, 'lxml')  # 以BeautifulSoup 解析 HTML 程式碼,lxml速度較快
        data = str(soup.find_all('select')).split('\n')
        symbol = '★'
        for i in data:
            if symbol in i:
                wash(cleanhtml(i))
