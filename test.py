from bs4 import BeautifulSoup
import requests


def cleaning(raw):
    left = raw.rfind('$')
    left2 = raw.find('$')
    right = raw.rfind(' ')
    money = raw[left:right].replace('◆', '').replace('★', '').replace('熱賣', '').strip()
    product = raw[:left2 - 2]
    coolpc[product] = money
    return product

coolpc = {}
keyword = input('請輸入要查詢的關鍵字').lower()

# 爬取網頁內容
r = requests.get('http://www.coolpc.com.tw/evaluate.php')

# 確認網頁狀態
if r.status_code == requests.codes.ok:

    # 以BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'lxml')

    data = (soup.find_all('option'))
    print(len(data))
    symbol = ['↪', '❤']

    for i in data:
        i = i.string
        if len(i) >2:
            cleaning(i)


    for j in coolpc:
        if keyword.lower() in j.lower() and not any(x in symbol for x in j):
            print(j, coolpc[j][1:])

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
