from bs4 import BeautifulSoup
import requests
import urllib.request as ur


newlist = []
newdict = {}

# 爬取網頁內容
r = requests.get('http://www.coolpc.com.tw/evaluate.php')

# 確認網頁狀態
if r.status_code == requests.codes.ok:

# 以BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'html.parser')

    soup2 = str(soup.find_all('select')).split('\n')
    for i in soup2:
        print('********'+i)





    # print(soup2)



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



