import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from seleniumrequests import Firefox
options = Options()
options.add_argument('-headless')

# from selenium.webdriver.chrome.options import Options
# chrome_options = Options() # 啟動無頭模式
# chrome_options.add_argument('--headless')  #規避google bug
# chrome_options.add_argument('--disable-gpu')
import requests
import re
tStart = time.time()#計時開始
# 爬取網頁內容
# r = requests.get('https://www.sinya.com.tw/show/?keyword=ASUS')

# 確認網頁狀態
# if r.status_code == requests.codes.ok:
#
# # 以BeautifulSoup 解析 HTML 程式碼
#     soup = BeautifulSoup(r.text, 'html.parser')

webdriver = Firefox(options=options)
# browser = webdriver.Chrome(options=chrome_options)
# browser.get("https://www.sinya.com.tw/diy")

response = webdriver.request('POST', 'https://www.sinya.com.tw/diy/show_option/', data={"prod_sub_slave_id": "148"})

response.encoding = 'utf-8'
print('OK')
# print(response.text)

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)
links = (soup.find_all('label', class_='showImg'))
# print(links)
# print(len(links))
# print(links[184].get('title').strip())
for link in links:
    print(link.get('title').strip())
# print(type(response))
# print(response.encoding)
# soup = BeautifulSoup(browser.page_source, "html.parser")
tEnd = time.time()#計時結束
#列印結果
print("It cost %f sec" % (tEnd - tStart))#會自動做近位
# print(soup)