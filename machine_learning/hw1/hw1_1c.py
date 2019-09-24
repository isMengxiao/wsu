# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

train = pd.read_csv("fashionmnist/fashion-mnist_train.csv")


def sign(w, x):
    if w*x >= 0:
        return 1
    else:
        return -1


train1 = train['label']
T = 20
y = []


for i in range(len(train1)):
    y.append(-1 if train1[i] % 2 else 1)
print(y)


w_av = 0
Mistake_AvePerc = [0] * T

for i in range(T):
    for j in range(len(train1)):
        y_av = sign(w_av, train1[j])
        if y_av != y[j]:
            w_av += y[j] * train1[j]
            Mistake_AvePerc[i] += 1
    print(Mistake_AvePerc[i], w_av)


