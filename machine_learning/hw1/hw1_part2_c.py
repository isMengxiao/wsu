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
w_av = np.zeros(shape=(10, 784))

# Initial the mistake record
Mistake_test_Perceptron = np.zeros(T)
Mistake_test_Average = np.zeros(T)

# Typical variable for average perceptron
c = 1
u = np.zeros(shape=(10, 784))
for iteration in range(T):
    #  train = shuffle(train)
    # Shuffle the training data for higher accurate,
    # but get lower accurate, so delete it.
    for i in range(len(train)):
        score_pe = 0  # used for record the maximum of argmax
        score_av = 0
        y_hat_pe = 0  # used for argmax
        y_hat_av = 0
        x = train.iloc[i][1:]
        y = train.iloc[i][0]
        # Compute the y_hat = argmax(w*x)
        for j in range(10):
            score_pe_new = np.dot(w_pe[j], x)
            score_av_new = np.dot(w_av[j], x)
            if score_pe_new >= score_pe:
                y_hat_pe = j
                score_pe = score_pe_new
            if score_av_new >= score_av:
                y_hat_av = j
                score_av = score_av_new
        if y_hat_pe != y:
            y_hat_pe = int(y_hat_pe)
            w_pe[y] += x
            w_pe[y_hat_pe] -= x
        if y_hat_av != y:
            y_hat_av = int(y_hat_av)
            w_av[y] += x
            w_av[y_hat_av] -= x
            u[y] += c * x
            u[y_hat_pe] -= c * x
        c += 1
    w_av -= (1/c) * u
    for i in range(len(test)):
        score_pe = 0  # used for record the maximum of argmax
        score_av = 0  # used for record the maximum of argmax
        y_hat_pe = 0  # used for argmax
        y_hat_av = 0  # used for argmax
        x = test.iloc[i][1:]
        y = test.iloc[i][0]
        # Compute the y_hat = argmax(w*x)
        for j in range(10):
            score_pe_new = np.dot(w_pe[j], x)
            score_av_new = np.dot(w_av[j], x)
            if score_pe_new >= score_pe:
                y_hat_pe = j
                score_pe = score_pe_new
            if score_av_new >= score_av:
                y_hat_av = j
                score_av = score_av_new
        if y_hat_pe != y:
            Mistake_test_Perceptron[iteration] += 1
        if y_hat_av != y:
            Mistake_test_Average[iteration] += 1
    w_av += (1/c) * u  # Prevent overfitting, we need to

print("The accuracy for standard perceptron:", \
      1-Mistake_test_Perceptron/len(test))
print("The accuracy for average percetpron:", \
      1-Mistake_test_Average/len(test))
end = datetime.datetime.now()
print("5.2 c:", start, end)
plt.figure(num=7)
plt.plot(1-Mistake_test_Perceptron/len(test), color="red", \
         label="Perceptron_test")
plt.plot(1-Mistake_test_Average/len(test), color="blue", \
         label="Averate-Perceptron_test")
plt.legend()
plt.xlabel('training iterations')
plt.ylabel('the mistake ratio')
plt.title("5.2-c Stand and Average Perceptron of 20 iterations")
plt.savefig('./part2_c.jpg')
plt.show()



