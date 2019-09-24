# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

train = pd.read_csv("fashionmnist/fashion-mnist_train.csv")


T = 50
y = []


for i in range(len(train)):
    y.append(-1 if train.iloc[i][0] % 2 else 1)
print(y)


w_pe = np.zeros(784)
w_pa = np.zeros(784)
Mistake_Perceptron, Mistake_PA = np.zeros(T), np.zeros(T)

for i in range(T):
    for j in range(len(train)):
        y_pe = 1 if np.dot(w_pe, train.iloc[j][1:]) >= 0 else -1
        y_pa = 1 if np.dot(w_pa, train.iloc[j][1:]) >= 0 else -1
        if y_pe != y[j]:
            w_pe += y[j] * train.iloc[j][1:]
            Mistake_Perceptron[i] += 1
        if y_pa != y[j]:
            w_pa += y[j] * train.iloc[j][1:] * \
                (1-y[j]*w_pa*train.iloc[j][1:]) / \
                (np.linalg.norm(train.iloc[j][1:])**2)
            Mistake_PA[i] += 1
#    print(i, Mistake_Perceptron[i], Mistake_PA[i], w_pe, w_pa)
plt.plot(Mistake_Perceptron)
plt.plot(Mistake_PA)
plt.show()

