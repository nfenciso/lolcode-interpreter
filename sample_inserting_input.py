# PROBABLY NOT THE BEST WAY

from tkinter import *
import os

ip = '192.168.1.1'

def get_info(arg):
    print(tfield.get("1.0", "current lineend"))

root = Tk()
tfield = Text(root)
tfield.pack()
f = os.popen('ping %s' % (ip))
for line in f:
    line = line.strip()
    if line:
        tfield.insert("end", line+"\n")
        # tfield.get("current linestart", "current lineend")
tfield.bind("<Return>", get_info)

root.mainloop()
f.close()