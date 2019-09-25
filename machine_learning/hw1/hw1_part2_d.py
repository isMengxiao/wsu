# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

import datetime
start = datetime.datetime.now()  # Record the start time.

train = pd.read_csv("data/fashion-mnist_train.csv")
test = pd.read_csv("data/fashion-mnist_test.csv")

T = 20  # Training iterations

# Initial the weight w.
w_pe = np.zeros(shape=(10, 784))
w_pa = np.zeros(shape=(10, 784))
w_av = np.zeros(shape=(10, 784))

# Initial the mistake record
Mistake_test_Perceptron = np.zeros(T*12)
Mistake_test_PA = np.zeros(T*12)
Mistake_test_Average = np.zeros(T*12)
Total_examples = np.linspace(5000, 5000*240, 240)

# Typical variable for average perceptron
c = 1
u = np.zeros(shape=(10, 784))
for iteration in range(T):
    # train = shuffle(train)  # Shuffle the training data for higher accurate
    for i in range(len(train)):
        score_pe = 0  # used for record the maximum of argmax
        score_pa = 0  # used for record the maximum of argmax
        score_av = 0
        y_hat_pe = 0  # used for argmax
        y_hat_pa = 0  # used for argmax
        y_hat_av = 0
        x = train.iloc[i][1:]
        y = train.iloc[i][0]
        # Compute the y_hat = argmax(w*x)
        for j in range(10):
            score_pe_new = np.dot(w_pe[j], x)
            score_pa_new = np.dot(w_pa[j], x)
            score_av_new = np.dot(w_av[j], x)
            if score_pe_new >= score_pe:
                y_hat_pe = j
                score_pe = score_pe_new
            if score_av_new >= score_av:
                y_hat_av = j
                score_av = score_av_new
            if score_pa_new >= score_pa:
                y_hat_pa = j
                score_pa = score_pa_new
        if y_hat_pe != y:
            y_hat_pe = int(y_hat_pe)
            w_pe[y] += x
            w_pe[y_hat_pe] -= x
        if y_hat_av != y:
            y_hat_av = int(y_hat_av)
            w_av[y] += x
            w_av[y_hat_av] -= x
            u[y] += c*x
            u[y_hat_pe] -= c*x
        if y_hat_pa != y:
            y_hat_pa = int(y_hat_pa)
            tao = (1 - np.dot(w_pa[y], x) + np.dot(w_pa[y_hat_pa], x)) \
                / (np.linalg.norm(x)**2)
            w_pa[y] += x * tao
            w_pa[y_hat_pa] -= x * tao
        c += 1
        w_av -= (1/c) * u
        if not (i+1) % 5000:
            for j in range(len(test)):
                score_pe = 0  # used for record the maximum of argmax
                score_pa = 0  # used for record the maximum of argmax
                score_av = 0
                y_hat_pe = 0  # used for argmax
                y_hat_pa = 0  # used for argmax
                y_hat_av = 0
                x = test.iloc[j][1:]
                y = test.iloc[j][0]
                # Compute the y_hat = argmax(w*x)
                for k in range(10):
                    score_pe_new = np.dot(w_pe[k], x)
                    score_pa_new = np.dot(w_pa[k], x)
                    score_av_new = np.dot(w_av[k], x)
                    if score_pe_new >= score_pe:
                        y_hat_pe = k
                        score_pe = score_pe_new
                    if score_pa_new >= score_pa:
                        y_hat_pa = k
                        score_pa = score_pa_new
                    if score_av_new >= score_av:
                        y_hat_av = k
                        score_av = score_av_new
                if y_hat_pe != y:
                    Mistake_test_Perceptron[iteration*12 + (i+1)//5000-1] += 1
                if y_hat_pa != y:
                    Mistake_test_PA[iteration*12 + (i+1)//5000-1] += 1
                if y_hat_av != y:
                    Mistake_test_Average[iteration*12 + (i+1)//5000-1] += 1
        w_av += (1/c) * u  # Prevent overfitting.

end = datetime.datetime.now()
print("5.2 d:", start, end)
plt.figure(num=8)
plt.plot(1 - Total_examples, Mistake_test_Perceptron/len(test), \
         color="red", label="Perceptron_test")
plt.plot(1 - Total_examples, Mistake_test_PA/len(test), color="blue", \
         label="Passive-Aggressive_test")
plt.plot(1 - Total_examples, Mistake_test_Average/len(test), color="green", \
         label="Average-Perceptron_test")
plt.legend(loc='upper right')
plt.xlabel('Number of training examples')
plt.ylabel('The testing accuracy')
plt.title("5.2-d Three test accuracy curve")
plt.savefig('./part2_d.jpg')
plt.show()



