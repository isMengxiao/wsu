# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


train = pd.read_csv("fashionmnist/fashion-mnist_train.csv")


T = 50
w = np.zeros(shape=(10, 784))
Mistake_Perceptron = np.zeros(T)


for i in range(T):
    for j in range(len(train)):
        yy = 0
        num = 0
        for k in range(10):
            y_new = np.dot(w[i], train.iloc[j][1:])
            if y_new >= yy:
                num = k
                yy = y_new
        if yy != train.iloc[j][0]:
            yy = int(yy)
            w[train.iloc[j][0]] += train.iloc[j][1:]
            w[yy] -= train.iloc[j][1:]
            Mistake_Perceptron[i] += 1
    print(i, Mistake_Perceptron[i], w)

