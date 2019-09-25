# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

train = pd.read_csv("data/fashion-mnist_train.csv")
test = pd.read_csv("data/fashion-mnist_test.csv")


T = 20  # Training iterations


y_train = np.zeros(len(train))  # Translate the label to (+1,-1)
y_test = np.zeros(len(train))
for i in range(len(train)):
    y_train[i] = -1 if train.iloc[i][0] % 2 else 1
for i in range(len(test)):
    y_test[i] = -1 if test.iloc[i][0] % 2 else 1


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
Mistake_test_Perceptron = np.zeros(T)
Mistake_test_PA = np.zeros(T)

for i in range(T):
    for j in range(len(train)):
        x = train.iloc[j][1:]
        if sign(w_pe, x) != y_train[j]:  # If Perceptron mistake
            w_pe += y_train[j] * x
            Mistake_Perceptron[i] += 1
        if sign(w_pa, x) != y_train[j]:  # If PA mistake
            w_pa += y_train[j] * np.dot(x, (1-y_train[j]*np.dot(w_pa, x))) / \
                    np.dot(x, x)
            Mistake_PA[i] += 1
    for j in range(len(test)):
        x = test.iloc[j][1:]
        if sign(w_pe, x) != y_test[j]:
            Mistake_test_Perceptron[i] += 1
        if sign(w_pa, x) != y_test[j]:
            Mistake_test_PA[i] += 1

plt.figure(num=2)
plt.plot(1-Mistake_Perceptron/len(train), color="red", label="Percetpron")
plt.plot(1-Mistake_test_Perceptron/len(test), color="red", \
         label="Perceptron-test", linestyle='--')
plt.plot(1-Mistake_PA/len(train), color="blue", label="Passive-Aggressive")
plt.plot(1-Mistake_test_PA/len(test), color="blue", \
         label="Passive-Aggressive_test", linestyle='--')
plt.legend()
plt.xlabel('training iterations')
plt.ylabel('the accuracy')
plt.title("5.1-b Binary classification")
plt.savefig('./part1_b.jpg')
plt.show()


