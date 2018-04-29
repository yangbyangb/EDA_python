__author__ = 'YB'
from tkinter import *
import pyEDA

window = Tk()

window.title("Python Spice")
window.geometry('800x500')
window.resizable(width=True, height=True)


def about():
    w = Label(window, text="开发者:\nYB")
    w.pack(side=TOP)


def new():
    pass


def myopen():
    pass


def save():
    pass


def save_as():
    pass


def close():
    pass


def settings():
    pass


def cut():
    pass


def copy():
    pass


def paste():
    pass


# 设置菜单栏
menubar = Menu(window)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=new)
filemenu.add_command(label="Open", command=myopen)
filemenu.add_command(label="Save", command=save)
filemenu.add_command(label="Save as...", command=save_as)
filemenu.add_command(label="Close", command=close)
filemenu.add_separator()
filemenu.add_command(label="Settings", command=settings)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=cut)
editmenu.add_command(label="Copy", command=copy)
editmenu.add_command(label="Paste", command=paste)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)

# 设置文本输入输出框
frame = Frame(height=700, width=1300, bg="white").pack(expand=YES, fill=BOTH)
inputbox = Text(window, width=42, height=24)
inputbox.place(x=8, y=54)
outputbox = Text(window, width=42, height=24)
outputbox.place(x=400, y=54)


def sim_plot():
    netlist = inputbox.get("0.0", "end")
    if __name__ == "__main__":
        outputbox.insert(END, 'py_spice>\n')
    pyEDA.simulate()


Button(window, text="simulate", bd=3, command=sim_plot).place(x=8, y=8)
Button(window, text="exit", width=5, bd=3, command=window.quit).place(x=700, y=8)

window['menu'] = menubar  # 指定顶层菜单
window.mainloop()
