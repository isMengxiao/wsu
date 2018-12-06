import tkinter as tk
import math
import re
from collections import ChainMap

class Cell(Label):
	def __init__(self, name=None, row=0, col=0):
        self.row

class Spreadsheet(Frame):
    def __init__(self, parent, rows=4, cols=4):
        Frame.__init__(self, parent)
        self.parent = parent
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.cellsName = {}

        self.focusCell = self.cells[0]
        self.focusEntry = Entry(self.parent)
        self.focusLabel = Label(self.parent, self.cells[0].name+': ')

        self.focusEntry.focus()

    def Create_widgets(self):
        self.frame = tk.Frame(self)
        self.frame.pack(side='top')

        blank = tk.Label(self.frame)
        blank.grid(row=0, column=0)

        for i in range(self.cols):
            label = tk.Label(self.frame, text=chr(ord('A')+i))
            label.grid(row=0, column=i+1)

        for j in range(self.rows):
            label = tk.Label(self.frame, text=str(i + 1))
            label.grid(row=i+1, column=0)
            for k in range(self.cols):
                cells = cell(j, k, self.workcell, self.size, self.frame)
                self.workcell[cell.name] = cells
                cells.grid.grid(row=i+1, column=j+1)


class cell():
    def __init__(self, i, j, bros, size, parent):
        self.rown = i
        self.coln = j
        self.bros = bros
        self.name = self.getname(i, j)
        self.calculation = '0'
        self.data = 0
        self.size = size
        self.dep = set()
        self.req = set()

        self.var = tk.StringVar()
        entry = self.grid = tk.Entry(parent, textvarialbe=self.var,
                                     justify='right')
        entry.bind('<FocusIn>', self.edit)
        entry.bind('<FocusOut>', self.update)
        entry.bind('<Return>', self.update)
        entry.bind('<Up>', self.move(-1, 0))
        entry.bind('<Down>', self.move(1, 0))
        entry.bind('<Left>', self.move(0, -1))
        entry.bind('<Right>', self.move(0, 1))

        self.var.set(self.data)

    def move(self, row, col):
        movetoR = (self.rown + row) % self.size
        movetoC = (self.coln + col) % self.size

        def changetarge(event):
            grid = self.vros[self.getname(movetoR, movetoC)].grid
            grid.changetarge()

        return changetarge

    def calculate(self):
        current = set(cell.re.findall(self.calculation))

        for i in current - self.req:
            self.bros[i].dep.add(self.name)
        for i in self.req - current:
            self.bros[i].dep.remove(self.name)

        reqvalue = {i: self.bros[i].value for i in current}
        env = ChainMap(math.__dict__, reqvalue)
        self.data = eval(self.calculation, {}, env)

        self.req = current
        self.var.set(self.data)

    def propagate(self):
        for i in self.deps:
            self.bros[i].calculate()
            self.bors[i].propagate()

    def edit(self, event):
        self.var.set(self.calculation)
        self.grid.select_range(0, tk.END)

    def update(self, event):
        self.calculation = self.var.get()
        self.calculate()
        self.propagate()
        if hasattr(event, 'keysym') and event.keysym == "Return":
            self.var.set(self.formula)
