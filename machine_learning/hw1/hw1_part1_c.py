# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

train = pd.read_csv("data/fashion-mnist_train.csv")
test = pd.read_csv("data/fashion-mnist_test.csv")


T = 20  # Training iterations


def sign(w, x):
    if np.dot(w, x) >= 0:
        return 1
    else:
        return -1

y_train = []  # Translate the label to (+1,-1)
y_test = []
for i in range(len(train)):
    y_train.append(1 if train.iloc[i][0]%2 else -1)
for i in range(len(test)):
    y_test.append(1 if test.iloc[i][0]%2 else -1)
print(y_train)

# initial the weight w.
w_pe = np.zeros(784)
w_av = np.zeros(784)

# Initial the mistake record
Mistake_test_Perceptron = np.zeros(T)
Mistake_test_Average = np.zeros(T)

# Initial the typical variables for Average-Perceptron
c = 1
u = np.zeros(784)

for i in range(T):
    for j in range(len(train)):
        #train = shuffle(train)
        x = train.iloc[j][1:]
        if sign(w_pe, x) != y_train[j]:
            w_pe += y_train[j] * x
        if sign(w_av, x) != y_train[j]:
            w_av += y_train[j] * x
            u += c * y_train[j] * x
        c += 1
    w_av -= (1/c) * u
    for j in range(len(test)):
        x = test.iloc[j][1:]
        if sign(w_pe, x) != y_test[j]:
            Mistake_test_Perceptron[i] += 1
        if sign(w_av, x) != y_test[j]:
            Mistake_test_Average[i] += 1
    # print(Mistake_test_Perceptron, Mistake_test_Average)
    # Since we still need more iteration, reset the weight
    # to prevent overfitting.
    w_av += (1/c) * u

print("Plain Perceptron :", 1-Mistake_test_Perceptron/len(test))
print("Average Perceptron: ", 1-Mistake_test_Average/len(test))
plt.figure(num=3)
plt.plot(1-Mistake_test_Perceptron/len(test), color="red", \
         label="Perceptron-test")
plt.plot(1-Mistake_test_Average/len(test), color="blue", \
         label="Average-Perceptron-test")
plt.legend()
plt.xlabel('training iterations')
plt.ylabel('the accuracy')
plt.title("5.1-c Accuracy curve for Plain and Average perceptron")
plt.savefig('./part1_c.jpg')
plt.show()




