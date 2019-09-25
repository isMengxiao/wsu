# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

train = pd.read_csv("data/fashion-mnist_train.csv")


T = 50  # Training iterations


y = np.zeros(len(train))  # Translate the label to (+1,-1)
for i in range(len(train)):
    y[i] = -1 if train.iloc[i][0] % 2 else 1
print(y)


def sign(w, x):
    if np.dot(w, x) >= 0:
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
    for j in range(len(train)):
        x = train.iloc[j][1:]
        if sign(w_pe, x) != y[j]:  # If Perceptron mistake
            w_pe += y[j] * x
            Mistake_Perceptron[i] += 1
        if sign(w_pa, x) != y[j]:  # If PA mistake
            w_pa += y[j] * np.dot(x, (1-y[j]*np.dot(w_pa, x))) / np.dot(x, x)
            Mistake_PA[i] += 1

plt.figure(num=1)
plt.plot(Mistake_Perceptron, color="red", label="Percetpron")
plt.plot(Mistake_PA, color="blue", label="Passive-Aggressive")
plt.legend()
plt.xlabel('training iterations')
plt.ylabel('the number of mistakes')
plt.title("5.1-a Binary classification")
plt.savefig('./part1_a.jpg')
plt.show()


