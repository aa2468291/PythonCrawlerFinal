from bs4 import BeautifulSoup
import requests
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def wash(raw):

  left = raw.rfind('$')
  left2 =raw.find('$')
  right = raw.rfind(' ')
  money = raw[left:right].replace('◆', '').replace('★', '').replace('熱賣', '').strip()
  product = raw[:left2-2]
  coolpc[product] = money


  return product


newlist = []
coolpc = {}

# 爬取網頁內容
r = requests.get('http://www.coolpc.com.tw/evaluate.php')

# 確認網頁狀態
if r.status_code == requests.codes.ok:

# 以BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'html.parser')


    soup2 = str(soup.find_all('select')).split('\n')
    filter = '★'
# any(x in (str(i)) for x in a)
    for i in soup2:
        if filter in i:
            wash(cleanhtml(i))
            # print('***'+money(cleanhtml(i)))
    for j in coolpc:
        print(j,coolpc[j])





    # print(soup2)

# print(coolpc)



    # soup2 = soup.find_all('select')
    # for select in soup.find('option'):
    #     newlist.append(select.string)
    #
    # print(newlist)
    #
    # print(soup.text)

    # soup3 = (soup2.split('\n'))
    # a = ['\u',]
    #
    # for check in soup3:
    #     if any(x in (str(row['NEW戶籍地址'])) for x in a)


    #
    # for i in newlist:
    #     print(i)



