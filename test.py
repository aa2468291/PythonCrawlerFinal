from bs4 import BeautifulSoup
import requests
import urllib.request as ur


# 爬取網頁內容
r = requests.get('https://www.coolpc.com.tw/evaluate.php')

# 確認網頁狀態
if r.status_code == requests.codes.ok:

# 以BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'html.parser')

    # print(soup.prettify())
    # print(soup.get_text())
    # print(soup.find_all('option'))
    for link in soup.find_all('option'):
        print(link.get_text())

