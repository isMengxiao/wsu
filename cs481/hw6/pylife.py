# -*- coding: utf-8 -*-
#! /usr/bin/env python3


from tkinter import *


class CellArray():
    def __init__(self, size=20):
        self.array = []
        self.initarray()

    def initarray(self):
        for i in range(self.size):
            self.array.append([])

class CellCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.initcolor = 'white'
        qbtn = Button(self, text='Quit', command=self.quit)
        sbtn = Button(self, text='Step', command=self.step)
        cbtn = Button(self, text='Clear',command=self.clear)



