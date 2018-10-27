# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import re

def concordance(f, unique = True):
    i = 0
    rdt = {}
    for lines in f:
        i += 1
        for a in re.split('\s|\n', lines):
            a = a.lower()
            if not a:
                break
            while not re.match('[a-zA-Z]', a):
                a = a[1:]
            while not re.match('[a-zA-Z]', a[::-1]):
                a = a[:-1]
            #print(a, end = '')
            if a not in rdt:
                rdt[a] = []
            if unique:
                if i not in rdt[a]:
                    #print('line:', i)
                    rdt[a].append(i)
            else:
                rdt[a].append(i)
    return rdt

if __name__ == '__main__':
    filepath = 'test1.txt'
    with open(filepath, 'r') as f:
        result = concordance(f)
        print(result)

