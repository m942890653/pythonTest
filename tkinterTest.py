# 导入tkinter模块的所有内容
import webbrowser
from tkinter import *


def callback():
    var.set("吹吧你，我才不信呢~")


root = Tk()

frame1 = Frame(root)
frame2 = Frame(root)

# 创建一个文本Label对象
var = StringVar()
var.set("您所下载的影片含有未成年人限制内容，\n请满18岁后再点击观看！")
textLabel = Label(frame1, textvariable=var, justify=LEFT)
textLabel.pack(side=LEFT)

# 创建一个图像Label对象

# 加一个按钮
theButton = Button(frame2, text="已满18周岁", command=callback)
theButton.pack()

frame1.pack(padx=10, pady=10)
frame2.pack(padx=10, pady=10)

# 复选框练习
GIRLS = ["西施", "王昭君", "貂蝉", "杨玉环"]
v = []
for girl in GIRLS:
    v.append(IntVar())
    b = Checkbutton(root, text=girl, variable=v[-1])
    b.pack(anchor=W)

# 单选框练习
v = IntVar()
Radiobutton(root, text="One", variable=v, value=1).pack(anchor=W)
Radiobutton(root, text="Two", variable=v, value=2).pack(anchor=W)
Radiobutton(root, text="Three", variable=v, value=3).pack(anchor=W)

# Listbox练习
sb = Scrollbar(root)
sb.pack(side=RIGHT, fill=Y)

lb = Listbox(root, yscrollcommand=sb.set)

for i in range(1000):
    lb.insert(END, str(i))

lb.pack(side=LEFT, fill=BOTH)
sb.config(command=lb.yview)

# Message练习
w2 = Message(root, text="这是一则骇人听闻的长长长长长消息！", width=100)
w2.pack()

# Spinbox练习
w = Spinbox(root, from_=0, to=10)
w.pack()

# webbrowser练习
text = Text(root, width=30, height=5)
text.pack()
text.insert(INSERT, "访问百度")
text.tag_add("link", "1.2", "1.10")
text.tag_config("link", foreground="blue", underline=True)


def show_arrow_cursor(event):
    text.config(cursor="arrow")


def show_xterm_cursor(event):
    text.config(cursor="xterm")


def click(event):
    webbrowser.open("http://www.baidu.com")


text.tag_bind("link", "<Enter>", show_arrow_cursor)
text.tag_bind("link", "<Leave>", show_xterm_cursor)
text.tag_bind("link", "<Button-1>", click)

mainloop()
