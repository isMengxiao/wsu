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
Mistake_test_Perceptron = np.zeros(T*12)
Mistake_test_PA = np.zeros(T*12)
Total_examples = np.linspace(1, 240, 240) * 5000

for i in range(T):
    for j in range(len(train)):
        x_train = train.iloc[j][1:]
        if sign(w_pe, x_train) != y_train[j]:
            w_pe += y_train[j] * x_train
        if sign(w_pa, x_train) != y_train[j]:
            w_pa += y_train[j] * np.dot(x_train, (1 - y_train[j] * \
                        np.dot(w_pa, x_train))) / np.dot(x_train, x_train)
        if not (j+1) % 5000:
            for k in range(len(test)):
                x_test = test.iloc[k][1:]
                if sign(w_pe, x_test) != y_test[k]:
                    Mistake_test_Perceptron[i*12 + (j+1)//5000 - 1] += 1
                if sign(w_pa, x_test) != y_test[k]:
                    Mistake_test_PA[i*12 + (j+1)//5000 - 1] += 1

plt.figure(num=4)
plt.plot(Total_examples, 1-Mistake_test_Perceptron/len(test), color="red", \
         label="Perceptron-test")
plt.plot(Total_examples, 1-Mistake_test_PA/len(test), color="blue", \
         label="Passive-Aggressive-test")
plt.legend()
plt.xlabel('training iterations')
plt.ylabel('the accuracy')
plt.title("5.1-d Accuracy curve")
plt.savefig('./part1_d.jpg')
plt.show()
