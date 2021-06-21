#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
import psutil
from seqtool.A1 import A1

main = Tk()
main.title('BasicQC')
main.geometry('1200x900')

if __name__ == '__main__':
    # 100 X 50 的 grid
    for i in range(50):
        main.rowconfigure(i, weight=1)
        for j in range(50):
            main.columnconfigure(j, weight=2)

    # notebook widget
    nb = ttk.Notebook(main)
    nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

    # add baseCall tab
    bcFrame = ttk.Frame(nb)
    nb.add(bcFrame, text='Run')
    bcTab = A1(main, bcFrame)
    bcTab.createTab()
    main.mainloop()
