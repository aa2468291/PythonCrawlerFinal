import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import requests
from bs4 import BeautifulSoup

window = tk.Tk()
window.title('PCDIY爬蟲比價系統 BY ADT105107 數位四甲 胡閔凱')
window.geometry('1920x1080')
window.configure()

headers = {'user-agent': 'Mozilla/5.0'}
sinyaData_list = []
sinyaData_sorted_list = []
sinyaData_url = []  # 圖片URL
coolpcData_list = []
coolpcData_sorted_list = []
control = False

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def cleaning(raw):
    left = raw.rfind('$')
    left2 = raw.find('$')
    right = raw.rfind(' ')

    if right < left:  # 避免沒撈到空格，造成left 反而比right大
        right = 100

    money = raw[left:right].replace('◆', '').replace('★', '').replace('熱賣', '').strip()[1:]
    product = raw[:left2 - 2]


    if is_integer(money) and  '↪' not in product and '❤' not in product and '共有商品' not in product:

        dict = {
            "name": product,
            "price": int(money),
        }

        coolpcData_list.append(dict)
        # coolpcData[product] = int(money)
    # 排除非商品的部分，確保所有money都是數字價錢的金額


def buttonHandler(eff=None, control = False):
    if control is True:
        image_url = 'https://www.sinya.com.tw' + str(sinyaData_url[int(sinya_listbox.curselection()[0])])
        pre_img = Image.open(requests.get(image_url, stream=True).raw)
        img = ImageTk.PhotoImage(pre_img.resize((300, 300), Image.ANTIALIAS))
        panel.configure(image=img)
        panel.image = img
        print('GET:'+image_url)
    else:
        print('Not Ready')


def coolpc():
    global coolpcData_sorted_list
    coolpcData_list.clear()
    coolpc_listbox.delete(0, 'end')
    print('原價屋資料撈取ing......')
    coolpc_listbox.insert(END, '原價屋資料撈取ing......')

    window.update()
    r = requests.get('https://www.coolpc.com.tw/evaluate.php')  # 爬取網頁內容
    if r.status_code == requests.codes.ok:  # 確認網頁狀態
        soup = BeautifulSoup(r.text, 'lxml')  # 以BeautifulSoup 解析 HTML 程式碼,lxml速度較快
        data = (soup.find_all('option'))
        # print(len(data))

        for i in data:
            i = i.string
            if len(i) > 2:
                cleaning(i)

    coolpcData_sorted_list = (sorted(coolpcData_list, key=lambda p: p['price']))
    # coolpcData_sorted = OrderedDict(sorted(coolpcData.items(), key=lambda x: x[1]))


    coolpc_listbox.insert(END, '原價屋資料撈取完畢!!!')
    window.update()
    coolpc_search()

    print('原價屋資料撈取完畢')


def sinya():
    global sinyaData_list
    global sinyaData_sorted_list
    global control
    control = False
    sinya_listbox.delete(0, 'end')
    r = requests.get('https://www.sinya.com.tw/diy', headers=headers)
    r.encoding = 'utf-8'  # 設定編碼為UTF-8
    pre_num = []  # 預計要爬取的ID list

    if r.status_code == requests.codes.ok:  # 確認網頁狀態
        sinyaData_list.clear()
        print('欣亞數位資料撈取ing , 約20秒')

        sinya_listbox.insert(END, '欣亞數位資料撈取ing , 約20秒')
        window.update()


        # 以BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'lxml')
        numbers = soup.find_all("div", class_="diy_class")
        for num in numbers:
            pre_num.append(num.get('data-id'))

        text = '資料清單共' + str(len(pre_num)) + '個，再等我一下......'
        print(text)

        sinya_listbox.insert(END, text)
        window.update()


        for checklist in pre_num:
            response = requests.post('https://www.sinya.com.tw/diy/show_option/', data={"prod_sub_slave_id": checklist}, headers=headers)
            checkid = 'ID:' + checklist + '=>GET !'
            sinya_listbox.insert(END, checkid)
            window.update()
            response.encoding = 'utf-8'
            soup2 = BeautifulSoup(response.text, 'lxml')




            items = (soup2.find_all('div', class_='prodClick'))
            for item in items:

                title = item.find('label', class_='showImg')
                i = (title.get('title').strip())
                img_url = title.get('rel').strip()
                price = title.parent.parent.parent.find('input', class_='prod_price_val')
                j = (price.get('value').strip())
                # sinyaData[i] = int(j)

                dict = {
                    "name": i,
                    "price": int(j),
                    "img_url": img_url
                }

                sinyaData_list.append(dict)



        # sinyaData_sorted = OrderedDict(sorted(sinyaData.items(), key=lambda x: x[1]))
        sinyaData_sorted_list = (sorted(sinyaData_list, key=lambda y: y['price']))







        # message1_label.configure(text=str(text)+',欣亞數位資料撈取完畢!!!')

        sinya_listbox.insert(END, '欣亞數位資料撈取完畢')
        window.update()
        control = True
        print('欣亞數位資料撈取完畢')
        sinya_search()


def coolpc_search():
    global coolpcData_sorted
    coolpc_listbox.delete(0, 'end')
    keyword = keyword_entry.get().lower().split()
    # symbol = ['↪', '❤', '共有商品']
    # and not any(x in j for x in symbol)
    # for j in coolpcData_sorted:
    #     if all(x in j.lower() for x in keyword):
    #         coolpc_listbox.insert(END, '$ '+str(coolpcData_sorted[j])+'  ///  '+str(j))

    for j in coolpcData_sorted_list:
        if all(x in j['name'].lower() for x in keyword):
            coolpc_listbox.insert(END, '$ '+str(j['price'])+'  ///  '+str(j['name']))

    window.update()


def sinya_search():
    sinya_listbox.delete(0, 'end')
    keyword = keyword_entry.get().lower().split()

    sinyaData_url.clear()


    for d in sinyaData_sorted_list:
        if all(x in d['name'].lower() for x in keyword):
            sinyaData_url.append(str(d['img_url']))
            sinya_listbox.insert(END, '$ ' + str(d['price']) + '  ///  ' + str(d['name']))

    window.update()



    # for k in sinyaData_sorted:
    #     if all(x in k.lower() for x in keyword):
    #         sinya_listbox.insert(END, '$ '+str(sinyaData_sorted[k])+'  ///  '+str(k))


def search_all(event=None):
    coolpc_search()
    sinya_search()


header_label = tk.Label(window, text='PCDIY爬蟲比價系統', font=("Helvetica", 32))
header_label.pack()

keyword_frame = tk.Frame(window)
keyword_frame.pack(side='top')
keyword_label = tk.Label(keyword_frame, text='請輸入要搜尋的商品，可以用空格多關鍵字搜尋(例如：華碩 i7 2070)', font=("微軟正黑體", 12))
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

coolpc_title_label = tk.Label(coolpc_list_frame, text='Coolpc原價屋', font=("微軟正黑體", 16), fg='blue')
coolpc_title_label.pack()


coolpc_scrollbar = Scrollbar(coolpc_list_frame)
coolpc_scrollbar.pack(side='right', fill='y')

coolpc_listbox = Listbox(coolpc_list_frame, width=80, height=35)
coolpc_listbox.pack(fill='y')

# for i in range(100):
#     coolpc_listbox.insert(END, i)

# attach listbox to scrollbar
coolpc_listbox.config(yscrollcommand=coolpc_scrollbar.set)
coolpc_scrollbar.config(command=coolpc_listbox.yview)
sinya_list_frame = tk.Frame(list_frame)
sinya_list_frame.pack(side='left', fill='y')

sinya_title_label = tk.Label(sinya_list_frame, text='Sinya欣亞數位', font=("微軟正黑體", 16), fg='green')
sinya_title_label.pack()

sinya_scrollbar = Scrollbar(sinya_list_frame)
sinya_scrollbar.pack(side='right', fill='y')

sinya_listbox = Listbox(sinya_list_frame, width=120, height=35)
sinya_listbox.bind('<<ListboxSelect>>', lambda eff: buttonHandler(eff, control=control))
sinya_listbox.pack(fill='y')

# for i in range(150):
#     sinya_listbox.insert(END, i)

# attach listbox to scrollbar
sinya_listbox.config(yscrollcommand=sinya_scrollbar.set)
sinya_scrollbar.config(command=sinya_listbox.yview)

work_frame = tk.Frame(window)
work_frame.pack()
work_label = tk.Label(work_frame, text='=====================================================================', font=("微軟正黑體", 24))
work_label.pack()

# message2_label = tk.Label(work_frame, text='')
# message2_label.pack()
# message3_label = tk.Label(work_frame, text='')
# message3_label.pack()
# message4_label = tk.Label(work_frame, text='')
# message4_label.pack()

get_btn = tk.Button(window, text='點我開始爬網站資料', command=lambda: [coolpc(), sinya()], font=("微軟正黑體", 14), relief='solid', fg='red')
get_btn.pack()

image_url = 'https://www.sinya.com.tw/upload/prod/Build.jpg'
pre_img = Image.open(requests.get(image_url, stream=True).raw)
img = ImageTk.PhotoImage(pre_img.resize((300, 300), Image.ANTIALIAS))

panel = Label(list_frame, image=img)
panel.pack(side='right')

window.mainloop()




















