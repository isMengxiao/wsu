# -*- coding: utf-8 -*-
#! /usr/bin/env python3

from tkinter import Tk

class TicTacToeBoard(tkinter.Frame):
    def __init__(self):



root = Tk()
root.title("Tic Tac Toe")
board = TicTacToeBoard(root)
board.grid


root.mainloop()
