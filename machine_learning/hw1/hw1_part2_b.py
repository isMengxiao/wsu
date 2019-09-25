# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime
start = datetime.datetime.now()  # Record the start time.

train = pd.read_csv("data/fashion-mnist_train.csv")
test = pd.read_csv("data/fashion-mnist_test.csv")

T = 20  # Training iterations

# Initial the weight w.
w_pe = np.zeros(shape=(10, 784))
w_pa = np.zeros(shape=(10, 784))

# Initial the mistake record
Mistake_Perceptron = np.zeros(T)
Mistake_PA = np.zeros(T)
Mistake_test_Perceptron = np.zeros(T)
Mistake_test_PA = np.zeros(T)

for iteration in range(T):
    for i in range(len(train)):
        score_pe = 0  # used for record the maximum of argmax
        score_pa = 0  # used for record the maximum of argmax
        y_hat_pe = 0  # used for argmax
        y_hat_pa = 0  # used for argmax
        x = train.iloc[i][1:]
        y = train.iloc[i][0]

        # Compute the y_hat = argmax(w*x)
        for j in range(10):
            score_pe_new = np.dot(w_pe[j], x)
            score_pa_new = np.dot(w_pa[j], x)
            if score_pe_new >= score_pe:
                y_hat_pe = j
                score_pe = score_pe_new
            if score_pa_new >= score_pa:
                y_hat_pa = j
                score_pa = score_pa_new
        if y_hat_pe != y:
            y_hat_pe = int(y_hat_pe)
            w_pe[y] += x
            w_pe[y_hat_pe] -= x
            Mistake_Perceptron[iteration] += 1
        if y_hat_pa != y:
            y_hat_pa = int(y_hat_pa)
            tao = (1 - np.dot(w_pa[y], x) + np.dot(w_pa[y_hat_pa], x)) \
                / (np.linalg.norm(x)**2)
            w_pa[y] += x * tao
            w_pa[y_hat_pa] -= x * tao
            Mistake_PA[iteration] += 1
    for i in range(len(test)):
        score_pe = 0  # used for record the maximum of argmax
        score_pa = 0  # used for record the maximum of argmax
        y_hat_pe = 0  # used for argmax
        y_hat_pa = 0  # used for argmax
        x = test.iloc[i][1:]
        y = test.iloc[i][0]

        # Compute the y_hat = argmax(w*x)
        for j in range(10):
            score_pe_new = np.dot(w_pe[j], x)
            score_pa_new = np.dot(w_pa[j], x)
            if score_pe_new >= score_pe:
                y_hat_pe = j
                score_pe = score_pe_new
            if score_pa_new >= score_pa:
                y_hat_pa = j
                score_pa = score_pa_new

        if y_hat_pe != y:
            Mistake_test_Perceptron[iteration] += 1
        if y_hat_pa != y:
            Mistake_test_PA[iteration] += 1

end = datetime.datetime.now()
print("5.2 b:", start, end)
plt.figure(num=6)
plt.plot(1-Mistake_Perceptron/len(train), color="red", label="Perceptron")
plt.plot(1-Mistake_test_Perceptron/len(test), color="red", \
         label="Perceptron_test", linestyle='--')
plt.plot(1-Mistake_PA/len(train), color="blue", label="Passive-Aggressive")
plt.plot(1-Mistake_test_PA/len(test), color="blue", \
         label="Passive-Aggressive_test", linestyle='--')
plt.legend(loc='upper right')
plt.xlabel('training iterations')
plt.ylabel('the number of mistakes')
plt.title("5.2-b four accuracy curves for 20 iterations")
plt.savefig('./part2_b.jpg')
plt.show()


