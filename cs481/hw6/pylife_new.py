# -*- coding: utf-8 -*-
#! /usr/bin/env python3
import tkinter as tk

class CellArray():
    def __init__(self, size=20):
        self.size = size
        self.Array = [[None for i in range(szie)] for j in range(size)]
        self.Arraylist = []
        self.Arraylist.append(self.Array)



class CellCanvas(Canvas):


