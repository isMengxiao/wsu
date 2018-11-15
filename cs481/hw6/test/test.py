# -*- coding: utf-8 -*-
#! /usr/bin/env python3


from tkinter import *

class test(Frame):
    def __init__(self, title='LIFEGAME'):
        super().__init__()
        t = tt()
        t.grid(row=0, column=0)
        qbtn = Button(self, text='Quit', command=self.quit)
        qbtn.grid(row=1, column=1)

class tt(Canvas):
    def __init__(self, size=20):
        super().__init__()
        bod = Canvas(self, width=100, heigh=100)
        self.cell=[]
        large=2
        self.size = size
        for i in range(self.size):
            self.cell.append([])
            for j in range(self.size):
                if j%2:
                    self.rec = self.create_rectangle(i*large, j*large, i+large, j+large, fill='black',
                                         command=self.changecolor())
                    self.cell[i].append(self.rec)
                else:
                    self.rec = self.create_rectangle(i*large, j*large, i+large, j+large, fill='white',
                                         command=self.changecolor())
                    self.cell[i].append(self.rec)

    def changecolor(self):
        print("he")
root = Tk()
root.title("lifeGame")
board = test(root)
board.grid()
root.mainloop()
