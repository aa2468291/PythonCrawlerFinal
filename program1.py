# prg#1

# ptt_movie 電影版爬蟲
import requests
from bs4 import BeautifulSoup

article_href = []
r = requests.get("https://www.ptt.cc/bbs/movie/index.html") #指定要抓取的版網址

soup = BeautifulSoup(r.text,"html.parser")
results = soup.select("div.title") # 指定抓取div.title部分網頁
print(results)

# 取出該頁所有的連結
for item in results:
    item_href = item.select_one("a").get("href")  # 取出 a href得料
    article_href.append(item_href)
print(article_href)