#! /usr/bin/env python3.6
from tkinter import Tk
from spreadsheet import Spreadsheet

root = Tk()
root.title("Spreadsheet Self-Test")
nRows = 4
nCols = 4
spreadsheet = Spreadsheet(root, nRows, nCols)
spreadsheet.grid(row=0, column=0, columnspan=nCols)
spreadsheet.focusLabel.grid(row=1, column=0)
spreadsheet.focusEntry.grid(row=1, column=1)
root.mainloop()
