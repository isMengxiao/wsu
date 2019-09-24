# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime

start = datetime.datetime.now()  # Record the start time.

train = pd.read_csv("fashionmnist/fashion-mnist_train.csv")
test = pd.read_csv("fashionmnist/fashion-mnist_test.csv")

t = 20  # for question 2,3,4
T = 50  # for question 1
"""
    Any variables end with pe or Perceptron is used for standard Perceptron
    Any variables end with pa or PA is used for Passive-Aggressive algorithm
    Any variables end with av or Av_Perceptron is used for averaged Perceptron

    If not mentioned, the variables are used for training.
    If the variables have 'test' as part of their name, it is used for test.

    I put all the four questions in the same iterations to save time.
"""
# Initial the weight w,
w_pe = np.zeros(shape=(10, 784))
w_pa = np.zeros(shape=(10, 784))
w_av = np.zeros(shape=(10, 784))

# Initial the mistake record for train.
Mistake_Perceptron = np.zeros(T)
Mistake_PA = np.zeros(T)
Mistake_Av_Perceptron = np.zeros(T)
# Initial the mistake record for test.
Mistake_test_Perceptron = np.zeros(t)
Mistake_test_PA = np.zeros(t)
Mistake_test_Av_Perceptron = np.zeros(t)

Mistake_test

# Start iterations.
for iteration in range(T):
    for j in range(len(train)):
        score_pe = 0
        score_pa = 0
        num_pe = 0
        num_pa = 0
        y = train.iloc[j][0]
        x = train.iloc[j][1:]
        for k in range(10):
            score_pe_new = np.dot(w_pe[k], x)
            score_pa_new = np.dot(w_pa[k], x)
            if score_pe_new >= score_pe:
                num_pe = k
                score_pe = score_pe_new
            if score_pa_new >= score_pa:
                num_pa = k
                score_pa = score_pa_new
        # start test mistake
        if num_pe != y:
            num_pe = int(num_pe)
            w_pe[y] += x
            w_pe[num_pe] -= x
            Mistake_Perceptron[iteration] += 1
        if num_pa != y:
            num_pa = int(num_pa)
            tao = (1 - np.dot(w_pa[y], x) + np.dot(w_pa[num_pa], x))\
                / (np.linalg.norm(x)**2)
            w_pa[y] += x * tao
            w_pa[num_pa] -= x * tao
            Mistake_PA[iteration] += 1


plt.plot(Mistake_Perceptron)
plt.plot(Mistake_PA)
plt.show()

end = datetime.datetime.now()

print(start)
print(end)
