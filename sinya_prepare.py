from bs4 import BeautifulSoup
import requests
import re

# 爬取網頁內容

pre_num = []
r = requests.get('https://www.sinya.com.tw/diy')
r.encoding = 'utf-8'

# 確認網頁狀態
if r.status_code == requests.codes.ok:

# 以BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all("div", class_="diy_class")
for link in links:
    pre_num.append(link.get('data-id'))

print(pre_num)
print(len(pre_num))



