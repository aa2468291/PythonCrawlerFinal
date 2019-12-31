from tkinter import *
import tkinter as tk

window = tk.Tk()
window.title('PCDIY爬蟲比價系統')
window.geometry('800x600')
window.configure()


header_label = tk.Label(window, text='PCDIY爬蟲比價系統')
header_label.pack()
keyword_frame = tk.Frame(window)
keyword_frame.pack(side='top')
keyword_label = tk.Label(keyword_frame, text='請輸入要搜尋的商品')
keyword_label.pack()



keyword_entry = tk.Entry(keyword_frame, width='40')
keyword_entry.pack(side='left')
submit_btn = tk.Button(keyword_frame, text='送出搜尋')
submit_btn.pack(side='left')

list_frame = tk.Frame(window)
list_frame.pack(side='top')


coolpc_list_frame = tk.Frame(list_frame)
coolpc_list_frame.pack(side='left', fill='y')

coolpc_scrollbar = Scrollbar(coolpc_list_frame)
coolpc_scrollbar.pack(side='right', fill='y')

coolpc_listbox = Listbox(coolpc_list_frame, width=20, height=20)
coolpc_listbox.pack(fill='y')

for i in range(100):
    coolpc_listbox.insert(END, i)

# attach listbox to scrollbar
coolpc_listbox.config(yscrollcommand=coolpc_scrollbar.set)
coolpc_scrollbar.config(command=coolpc_listbox.yview)
sinya_list_frame = tk.Frame(list_frame)
sinya_list_frame.pack(side='right', fill='y')
sinya_scrollbar = Scrollbar(sinya_list_frame)
sinya_scrollbar.pack(side='right', fill='y')

sinya_listbox = Listbox(sinya_list_frame, width=20, height=20)
sinya_listbox.pack(fill='y')

for i in range(150):
    sinya_listbox.insert(END, i)

# attach listbox to scrollbar
sinya_listbox.config(yscrollcommand=sinya_scrollbar.set)
sinya_scrollbar.config(command=sinya_listbox.yview)

work_frame = tk.Frame(window)
work_frame.pack()
work_label = tk.Label(work_frame, text='=========系統訊息==========')
work_label.pack()
window.mainloop()
