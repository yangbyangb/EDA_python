__author__ = 'YB'
from tkinter import *
from tkinter import filedialog
import pyEDA

window = Tk()

window.title("Python Spice")
window.geometry('850x500')
window.resizable(width=True, height=True)


def _about():
    w = Label(window, text="开发者:\nYB")
    w.pack(side=TOP)


def _open():
    window.filename = filedialog.askopenfilename(initialdir="~/PycharmProjects", title="Select file",
                                                 filetypes=(("netlist files", "*.sp"), ("all files", "*.*")))
    print(window.filename)
    file = open(window.filename, "r")
    netlist = []
    while True:
        line = file.readline()
        netlist += line
        if len(line) == 0:
            break


def _save():
    window.filename = filedialog.asksaveasfilename(initialdir="~/PycharmProjects", title="Select file",
                                                   filetypes=(("netlist files", "*.sp"), ("all files", "*.*")))


def _save_as():
    window.filename = filedialog.asksaveasfilename(initialdir="~/PycharmProjects", title="Select file",
                                                   filetypes=(("netlist files", "*.sp"), ("all files", "*.*")))


def _close():
    pass


def _settings():
    pass


def _cut():
    pass


def _copy():
    pass


def _paste():
    pass


# 设置菜单栏
menubar = Menu(window)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=_open)
filemenu.add_command(label="Save", command=_save)
filemenu.add_command(label="Save as...", command=_save_as)
filemenu.add_command(label="Close", command=_close)
filemenu.add_separator()
filemenu.add_command(label="Settings", command=_settings)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=_cut)
editmenu.add_command(label="Copy", command=_copy)
editmenu.add_command(label="Paste", command=_paste)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=_about)
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)

# 设置文本输入输出框
frame = Frame(height=700, width=1400, bg="white").pack(expand=YES, fill=BOTH)
inputbox = Text(window, width=42, height=24)
inputbox.place(x=8, y=54)
outputbox = Text(window, width=48, height=24)
outputbox.place(x=400, y=54)


def sim_plot():
    netlist = inputbox.get("0.0", "end")
    if __name__ == "__main__":
        inputbox.insert('0.0', window.filename)
    if __name__ == "__main__":
        outputbox.insert(END, 'py_spice >\n')
        outputbox.insert(END, '    ' + window.filename + '\n')
    pyEDA.simulate()


Button(window, text="simulate", bd=3, command=sim_plot).place(x=8, y=8)
Button(window, text="exit", width=5, bd=3, command=window.quit).place(x=700, y=8)

window['menu'] = menubar  # 指定顶层菜单
window.mainloop()
