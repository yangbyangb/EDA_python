from tkinter import *
import parser
import stamp

# problems:
# db 
# fake v_ac implementation

window = Tk()
window.geometry('590x400')
window.title('Spice')
frame = Frame(height=700, width=1300, bg="white").pack(expand=YES, fill=BOTH)
inputbox = Text(window, width=42, height=24)
inputbox.place(x=8, y=8)
outputbox = Text(window, width=32, height=26)
outputbox.place(x=330, y=8)

n = 0
node_list = []
all_dev_list = []
device_list = []
device_node_list = []
command = 0


def func_simulate():
    netlist = inputbox.get("0.0", "end")
    if __name__ == "__main__":
        outputbox.insert(END, '\n--------parse-------');
        n, node_list, all_dev_list, device_list, device_node_list, command, fstart, fstop, fnodes, tstart, tstop, tstep = parser.doparse(
            netlist);
        outputbox.insert(END, "\n\ndevices:")
        outputbox.insert(END, all_dev_list)
        outputbox.insert(END, "\n\nnodes:")
        outputbox.insert(END, node_list)
    if __name__ == "__main__":
        outputbox.insert(END, '\n\n----stamp&calculate---');
        res_string = stamp.dostamp(netlist, n, node_list, device_list, device_node_list, command, fstart, fstop, fnodes,
                                   tstart, tstop, tstep)
        outputbox.insert(END, res_string)


b1 = Button(window, text="simulate", width=10, height=1, command=func_simulate)
b1.place(x=100, y=352)
window.mainloop()
