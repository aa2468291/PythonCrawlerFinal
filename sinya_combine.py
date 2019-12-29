from bs4 import BeautifulSoup
import requests
import time
from seleniumrequests import Firefox
from selenium.webdriver.firefox.options import Options
tStart = time.time()  # 計時開始
options = Options()
options.add_argument('-headless')  # FIREFOX 改成headless mode
webdriver = Firefox(options=options)

r = requests.get('https://www.sinya.com.tw/diy')
r.encoding = 'utf-8'  # 設定編碼為UTF-8

pre_num = []  # 預計要爬取的ID list
products = []

# 確認網頁狀態
if r.status_code == requests.codes.ok:

    # 以BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'lxml')
    numbers = soup.find_all("div", class_="diy_class")
    for num in numbers:
        pre_num.append(num.get('data-id'))

    print(pre_num)

    for checklist in pre_num:
        response = webdriver.request('POST', 'https://www.sinya.com.tw/diy/show_option/',
                                     data={"prod_sub_slave_id": checklist})
        response.encoding = 'utf-8'
        soup2 = BeautifulSoup(response.text, 'lxml')
        items = (soup2.find_all('label', class_='showImg'))
        for item in items:
            print(item.get('title').strip())
            # products.append(item.get('title').strip())
        print('********************************************************')

tEnd = time.time()  # 計時結束
# print(products)




print("It cost %f sec" % (tEnd - tStart))  # 會自動做近位