# -*- coding: utf-8 -*-
#! /usr/bin/env python3


from tkinter import *

class Cell:
    def __init__(self, status=0, prestatus=0, x=0, y=0):
        self.status = status
        self.prestatus = []
        self.prestatus.append(prestatus)
        self.place = (x, y)

    def step(self, status=0):
        self.prestatus.append(self.status)
        self.status = status

class CellArray:
    def __init__(self, size=20):
        self.array = []
        self.size = size
        self.initarray()

    def initarray(self):
        for i in range(self.size):
            self.array.append([])
            for j in range(self.size):
                self.array[i].append(a = Cell(0, i, j))

    def checkneighbour(self, x, y):
        sum = 0
        s = [(x+1, y), (x+1, y-1), (x, y-1),
             (x-1, y-1), (x-1, y), (x-1, y+1),
             (x, y+1), (x+1, y+1)]
        for (a, b) in s:
            if 0<=a<=self.size and 0<=b<=self.size:
                if self.array[a][b].status:
                    sum += 1
        if self.array[x][y].status and sum >= 2:
            self.array[x][y].step(1)
        elif sum >= 3:
            self.array[x][y].step(1)
        else:
            self.array[x][y].step()

    def step(self):
        for i in range(self.size):
            for j in range(self.size):
                self.checkneighbour(i, j)

class CellCanvas(Canvas):
    def __init__(self, size=20, blk_size=1):
        super().__init__()
        board = Canvas(self, width=720, height=720)
        board.grid(row=0, column=0)
        self.size = size
        self.blk_size  = blk_size
        self.cells = []
        for i in range(size):
            self.cells.append([])
            for j in range(size):
                self.cells[i].append([])
                if j%2:
                    self.cells[i][j] = self.create_rectangle(i, j, i+self.blk_size,
                                          j+self.blk_size, fill='black')
                    self.cells[i][j].grid(row=i, column=j)
                else:
                    self.cells[i][j] = self.create_rectangle(i, j, i+self.blk_size,
                                          j+self.blk_size, fill='white')
                    self.cells[i][j].grid(row=i, column=j)



class MainBoard(Frame):
    def __init__(self, title='Life Game'):
        super().__init__()
        board = CellCanvas()
        board.grid(row=0, column=0)
        qbtn = Button(self, text='Quit', command=self.quit)
       # sbtn = Button(self, text='Step', command=self.step)
       # cbtn = Button(self, text='Clear',command=self.clear)
        qbtn.grid(row=1, column=1)
       # sbtn.grid(row=1, column=2)
       # cbtn.gird(row=1, column=3)


root = Tk()
root.title("Life game")
board = MainBoard(root)
board.grid()
root.mainloop()




