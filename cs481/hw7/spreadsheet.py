from tkinter import *
import math
from dependencies import dependersOn

class Cell():
    def __init__(self, name, row, col, expr='', parent= None):
        self.row = row
        self.col = col
        self.name = name
        self.expr = expr
        self.parent = parent

        entry = self.grid = Entry(self.parent)
        entry.bind('<Up>')
        entry.bind('<Down>')
        entry.bind('<Left>')
        entry.bind('<Right>')

    def __str__(self):
        value = spreadsheet.symbol_table[self.name]
        return 'name:%s, expr: %s, avlue: %d' %(self.name, self.expr, value)

    def update(self):
        value = spreadsheet.symbol_table[self.name]
        if value.__name__ == 'function':
            self.grid['text'] = self.expr
        elif value is None:
            self.grid['text'] = ''
        else:
            self.grid['text'] = str(value)

class Spreadsheet(Frame):
    def __init__(self, parent, rows=4, cols=4):
        Frame.__init__(self, parent)
        self.parent = parent
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.cellsName = []
        self.symbol_table = {}
        self.deps = {}

        self.Create_widgets()
        self.focusCell = self.cells[0]
        self.focusEntry = Entry(self.parent)
        print('name',self.cells[0].name)
        self.focusLabel = Label(self.parent, self.cells[0].name+': ')
        self.focusEntry.focus()


    def Create_widgets(self):
        rowlabel = 'abcdefghijklmnopqrstuvwxyz'
        for col in range(self.cols):
            label = Label(self)
            label['text'] = int(col)
            label.grid(row=0, column=col+1)
        for row in range(self.rows):
            label = Label(self)
            print(row)
            label['text'] = rowlabel[row]
            label.grid(row=row+1, column=0)
        for col in range(self.cols):
            for row in range(self.rows):
                name=rowlabel[row] + str(col)
                cell = Cell(self, name, row, col, parent=self.parent)
                self.cells.append(cell)
                #cell.grid(row=row+1, column=col+1)
                self.cellsName.append(name)
                self.symbol_table[cell.name] = ''
                self.deps[cell] = set()


    def update(self, cell, expr):
        """
        pre_expr = cell.expr
        pre_value = self.symbol_table[cell.name]
        pre_code = cell.code
        pre_deps = self.deps[cell]
        """
        cell.expr = expr
        newcode = compile(expr, cell.name, 'eval')
        self.symbol_table[cell.name] = eval(newcode, {}, self.symbol_table)
        cell.update()
        for row in self.rows:
            for col in self.cols:
                cell = self.cells[col][row]
                self.deps[cell] = (dependersOn(cell.name, deps))
        for acell in dependersOn(cell, self.deps):
            self.symbol_table[acell.name] = eval(acell.expr, {}, self.symbol_table)
            acell.update()

    def focuschange(self, cell):
        self.focusCell['background'] = 'white'
        self.focusCell = cell
        self.focusCell['background'] = 'yellow'
        self.focusLabel['text'] = cell.name
        self.focusEntry.delete(0, End)
        self.focusEntry.insert(End, cell.expr)


    def __str__(self):
        result = ''
        for cell in self.cells:
            result += str(cell) + ',\n'
        return result

if __name__ == '__main__':
    print('helloworld')
