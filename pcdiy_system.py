from bs4 import BeautifulSoup
import requests
import time
import re

coolpcData = {}
sinyaData = {}



def cleaning(raw):
    left = raw.rfind('$')
    left2 = raw.find('$')
    right = raw.rfind(' ')
    money = raw[left:right].replace('◆', '').replace('★', '').replace('熱賣', '').strip()
    product = raw[:left2 - 2]
    coolpcData[product] = money


def coolpc():

    print('原價屋資料撈取ing......')
    r = requests.get('http://www.coolpc.com.tw/evaluate.php')  # 爬取網頁內容
    if r.status_code == requests.codes.ok:  # 確認網頁狀態
        soup = BeautifulSoup(r.text, 'lxml')  # 以BeautifulSoup 解析 HTML 程式碼,lxml速度較快
        data = (soup.find_all('option'))
        # print(len(data))

        for i in data:
            i = i.string
            if len(i) > 2:
                cleaning(i)

    print('原價屋資料撈取完畢')



def sinya():
    r = requests.get('https://www.sinya.com.tw/diy')
    r.encoding = 'utf-8'  # 設定編碼為UTF-8

    pre_num = []  # 預計要爬取的ID list

    if r.status_code == requests.codes.ok:   # 確認網頁狀態
        print('欣亞數位資料撈取ing , 約20秒')

        # 以BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'lxml')
        numbers = soup.find_all("div", class_="diy_class")
        for num in numbers:
            pre_num.append(num.get('data-id'))

        print('資料清單共'+str(len(pre_num))+'個...，還在努力撈取中')

        for checklist in pre_num:
            response = requests.post('https://www.sinya.com.tw/diy/show_option/', data={"prod_sub_slave_id": checklist})
            response.encoding = 'utf-8'
            soup2 = BeautifulSoup(response.text, 'lxml')

            items = (soup2.find_all('div', class_='prodClick'))
            for item in items:
                title = item.find('label', class_='showImg')
                i = (title.get('title').strip())
                price = title.parent.parent.parent.find('input', class_='prod_price_val')
                j = (price.get('value').strip())
                sinyaData[i] = j
        print('欣亞數位資料撈取完畢')




def coolpc_search(keyword):
    symbol = ['↪', '❤']
    for j in coolpcData:
        if keyword.lower() in j.lower() and not any(x in symbol for x in j):
            print(j, coolpcData[j][1:])

def sinya_search(keyword):
    for k in sinyaData:
        if keyword.lower() in k.lower():
            print(k, sinyaData[k])

coolpc()
sinya()


while True:
    search = input('請輸入要查詢的關鍵字').lower()
    print('================以下是原價屋的相關查詢結果==================')
    coolpc_search(search)
    print('================以下是欣亞數位的相關查詢結果================')
    sinya_search(search)
    print('================結束，還有需要查詢的嗎？====================')


