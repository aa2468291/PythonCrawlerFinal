from bs4 import BeautifulSoup
import requests
import time
# from seleniumrequests import Firefox
# from selenium.webdriver.firefox.options import Options
tStart = time.time()  # 計時開始
# options = Options()
# options.add_argument('-headless')  # FIREFOX 改成headless mode
# webdriver = Firefox(options=options)

r = requests.get('https://www.sinya.com.tw/diy')
r.encoding = 'utf-8'  # 設定編碼為UTF-8

pre_num = []  # 預計要爬取的ID list
products = []
sinya = {}

# 確認網頁狀態
if r.status_code == requests.codes.ok:
    print('資料撈取ing,約20秒')

    # 以BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'lxml')
    numbers = soup.find_all("div", class_="diy_class")
    for num in numbers:
        pre_num.append(num.get('data-id'))

    print(pre_num)

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
            sinya[i] = j

print('資料撈取完畢')
tEnd = time.time()  # 計時結束

print("總共花了 %f 秒" % (tEnd - tStart))  # 會自動做近位
keyword = input('請輸入要查詢的關鍵字')

for k in sinya:
    if keyword.lower() in k.lower():
        print(k, sinya[k])





