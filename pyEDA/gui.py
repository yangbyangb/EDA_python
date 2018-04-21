import tkinter
import pyEDA

root = tkinter.Tk()

root.title("Python Spice by YB")
root.geometry('800x800')
root.resizable(width=True, height=True)  # 宽不可变, 高可变

fm = tkinter.Frame(root)

fm1 = tkinter.Frame(root)
t_left = tkinter.Text().grid(row=1, column=1)
t_right = tkinter.Text().grid(row=2, column=1)
fm1.grid(row=2, column=1)

fm2 = tkinter.Frame(root)
tkinter.Button(root, text="simulate", bd=3, command=pyEDA.simulate).grid(row=1, column=2)
fm1.grid(row=1, column=2)

fm.grid(row=2, column=2)

root.mainloop()
