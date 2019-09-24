# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

train = pd.read_csv("data/fashion-mnist_train.csv")


T = 50  # Training iterations


y = []  # Translate the label to (+1,-1)
for i in range(len(train)):
    y.append(-1 if train.iloc[i][0] % 2 else 1)

def sign(w, x):
    if sum(w*x) >= 0:
        return 1
    else:
        return -1


# initial the weight w.
w_pe = np.zeros(784)
w_pa = np.zeros(784)

# Initial the mistake record
Mistake_Perceptron = np.zeros(T)
Mistake_PA = np.zeros(T)

for i in range(T):
    MP = 0
    MA = 0
    for j in range(len(train)):
        x = train.iloc[j][1:]
        y_pe = sign(w_pe, x)
        y_pa = sign(w_pa, x)
        if y_pe != y[j]:  # If Perceptron mistake
            w_pe += y[j] * x
            Mistake_Perceptron[i] += 1
        if y_pa != y[j]:  # If PA mistake
            w_pa += y[j] * x * (1-y[j]*w_pa*x) / np.dot(x, x)
            Mistake_PA[i] += 1
    #print(Mistake_Perceptron[i], Mistake_PA[i])
plt.figure(num=1)
plt.plot(Mistake_Perceptron, color="red", label="Percetpron")
plt.plot(Mistake_PA, color="blue", label="Passive-Aggressive")
plt.legend()
plt.xlabel('training iterations')
plt.ylabel('the number of mistakes')
plt.title("5.1-a Binary classification")
plt.savefig('./part1_a.jpg')
plt.show()


