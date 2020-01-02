from tkinter import *
import tkinter as tk
from bs4 import BeautifulSoup
import requests

window = tk.Tk()
window.title('PCDIY爬蟲比價系統')
window.geometry('1920x1080')
window.configure()

coolpcData = {}
sinyaData = {}


def cleaning(raw):
    left = raw.rfind('$')
    left2 = raw.find('$')
    right = raw.rfind(' ')
    money = raw[left:right].replace('◆', '').replace('★', '').replace('熱賣', '').strip()[1:]
    product = raw[:left2 - 2]
    coolpcData[product] = money


def coolpc():
    print('原價屋資料撈取ing......')
    message1_label = tk.Label(work_frame, text='原價屋資料撈取ing......', font=("微軟正黑體", 12))
    message1_label.pack()

    # message1_label.configure(text='原價屋資料撈取ing......')
    window.update()
    r = requests.get('http://www.coolpc.com.tw/evaluate.php')  # 爬取網頁內容
    if r.status_code == requests.codes.ok:  # 確認網頁狀態
        soup = BeautifulSoup(r.text, 'lxml')  # 以BeautifulSoup 解析 HTML 程式碼,lxml速度較快
        data = (soup.find_all('option'))
        # print(len(data))

        for i in data:
            i = i.string
            if len(i) > 2:
                cleaning(i)


    message2_label = tk.Label(work_frame, text='原價屋資料撈取完畢!!!', font=("微軟正黑體", 12))
    message2_label.pack()
    window.update()

    coolpc_search()

    print('原價屋資料撈取完畢')


def sinya():
    r = requests.get('https://www.sinya.com.tw/diy')
    r.encoding = 'utf-8'  # 設定編碼為UTF-8
    pre_num = []  # 預計要爬取的ID list

    if r.status_code == requests.codes.ok:  # 確認網頁狀態

        print('欣亞數位資料撈取ing , 約20秒')
        message3_label = tk.Label(work_frame, text='欣亞數位資料撈取ing , 約20秒', font=("微軟正黑體", 12))
        message3_label.pack()
        window.update()


        # 以BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'lxml')
        numbers = soup.find_all("div", class_="diy_class")
        for num in numbers:
            pre_num.append(num.get('data-id'))

        text = '資料清單共' + str(len(pre_num)) + '個，再等我一下......'
        print(text)
        message4_label = tk.Label(work_frame, text=text, font=("微軟正黑體", 12))

        message4_label.pack()
        window.update()


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

        # message1_label.configure(text=str(text)+',欣亞數位資料撈取完畢!!!')
        message5_label = tk.Label(work_frame, text='欣亞數位資料撈取完畢', font=("微軟正黑體", 12))
        message5_label.pack()
        window.update()
        print('欣亞數位資料撈取完畢')
        sinya_search()


def coolpc_search():
    coolpc_listbox.delete(0, 'end')
    keyword = keyword_entry.get().lower().split()
    symbol = ['↪', '❤', '共有商品']
    for j in coolpcData:
        if all(x in j.lower() for x in keyword) and not any(x in j for x in symbol):
            coolpc_listbox.insert(END, '$ '+str(coolpcData[j])+'  ///  '+str(j))


def sinya_search():
    sinya_listbox.delete(0, 'end')
    keyword = keyword_entry.get().lower().split()
    for k in sinyaData:
        if all(x in k.lower() for x in keyword):
            sinya_listbox.insert(END, '$ '+str(sinyaData[k])+'  ///  '+str(k))


def search_all(event=None):
    coolpc_search()
    window.update()
    sinya_search()
    window.update()


header_label = tk.Label(window, text='PCDIY爬蟲比價系統', font=("Helvetica", 32))
header_label.pack()

keyword_frame = tk.Frame(window)
keyword_frame.pack(side='top')
keyword_label = tk.Label(keyword_frame, text='請輸入要搜尋的商品，可以用空格多關鍵字搜尋', font=("微軟正黑體", 12))
keyword_label.pack()

keyword_entry = tk.Entry(keyword_frame, width='40', font=("微軟正黑體", 16))
keyword_entry.pack(side='left')
submit_btn = tk.Button(keyword_frame, text='送出搜尋', command=lambda: [coolpc_search(), sinya_search()], font=("微軟正黑體", 12), relief='solid')
submit_btn.pack(side='left')

keyword_entry.bind("<Return>", search_all)


list_frame = tk.Frame(window)
list_frame.pack(side='top')


coolpc_list_frame = tk.Frame(list_frame)
coolpc_list_frame.pack(side='left', fill='y')

coolpc_title_label = tk.Label(coolpc_list_frame, text='原價屋', font=("微軟正黑體", 16), fg='blue')
coolpc_title_label.pack()


coolpc_scrollbar = Scrollbar(coolpc_list_frame)
coolpc_scrollbar.pack(side='right', fill='y')

coolpc_listbox = Listbox(coolpc_list_frame, width=80, height=20)
coolpc_listbox.pack(fill='y')

# for i in range(100):
#     coolpc_listbox.insert(END, i)

# attach listbox to scrollbar
coolpc_listbox.config(yscrollcommand=coolpc_scrollbar.set)
coolpc_scrollbar.config(command=coolpc_listbox.yview)
sinya_list_frame = tk.Frame(list_frame)
sinya_list_frame.pack(side='right', fill='y')

sinya_title_label = tk.Label(sinya_list_frame, text='欣亞數位', font=("微軟正黑體", 16), fg='green')
sinya_title_label.pack()

sinya_scrollbar = Scrollbar(sinya_list_frame)
sinya_scrollbar.pack(side='right', fill='y')

sinya_listbox = Listbox(sinya_list_frame, width=150, height=20)
sinya_listbox.pack(fill='y')

# for i in range(150):
#     sinya_listbox.insert(END, i)

# attach listbox to scrollbar
sinya_listbox.config(yscrollcommand=sinya_scrollbar.set)
sinya_scrollbar.config(command=sinya_listbox.yview)

work_frame = tk.Frame(window)
work_frame.pack()
work_label = tk.Label(work_frame, text='=========系統訊息==========', font=("微軟正黑體", 24))
work_label.pack()

# message2_label = tk.Label(work_frame, text='')
# message2_label.pack()
# message3_label = tk.Label(work_frame, text='')
# message3_label.pack()
# message4_label = tk.Label(work_frame, text='')
# message4_label.pack()

get_btn = tk.Button(window, text='點我開始爬網站資料', command=lambda: [coolpc(), sinya()], font=("微軟正黑體", 14), relief='solid', fg='red')
get_btn.pack()
window.mainloop()




















