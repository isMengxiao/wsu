# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

train = pd.read_csv("fashionmnist/fashion-mnist_train.csv")
test = pd.read_csv("fashionmnist/fashion-mnist_test.csv")


T = 20
y = []


for i in range(len(train)):
    y.append(-1 if train.iloc[i][0] % 2 else 1)
print(y)


w_pe = np.zeros(784)
w_pa = np.zeros(784)
w_avp = np.zeros(784)
u = np.zeros(784)

Mistake_Perceptron = np.zeros(T)
Mistake_PA = np.zeros(T)
Mistake_Av_Perceptron = np.zeros(T)

w_pe_final = np.zeros(shape=(T, 784))
w_pa_final = np.zeros(shape=(T, 784))
w_avp_final = np.zeros(shape=(T, 784))

Mistake_Perceptron_test = np.zeros(T)
Mistake_PA_test = np.zeros(T)
Mistake_Av_Perceptron_test = np.zeros(T)

c = 1

for i in range(T):
    for j in range(len(train)):
        y_pe = 1 if np.dot(w_pe, train.iloc[j][1:]) >= 0 else -1
        y_pa = 1 if np.dot(w_pa, train.iloc[j][1:]) >= 0 else -1
        y_avp = 1 if np.dot(w_avp, train.iloc[j][1:]) >= 0 else -1

        if y_pe != y[j]:
            w_pe += y[j] * train.iloc[j][1:]
            Mistake_Perceptron[i] += 1

        if y_pa != y[j]:
            w_pa += y[j] * train.iloc[j][1:] * \
                (1-y[j]*w_pa*train.iloc[j][1:]) / \
                (np.linalg.norm(train.iloc[j][1:])**2)
            Mistake_PA[i] += 1

        if y_avp != y[j]:
            w_avp += y[j] * train.iloc[j][1:]
            u += y[j] * train.iloc[j][1:] * c
            Mistake_Av_Perceptron[i] += 1

        if i >= 1:
            y_pe_test = 1 if \
                np.dot(w_pe_final[i-1], train.iloc[j][1:]) >= 0 else -1
            y_pa_test = 1 if \
                np.dot(w_pa_final[i-1], train.iloc[j][1:]) >= 0 else -1
            y_avp_test = 1 if \
                np.dot(w_avp_final[i-1], train.iloc[j][1:]) >= 0 else -1

            if y_pe_test != y[j]:
                Mistake_Perceptron_test[i-1] += 1
            if y_pa_test != y[j]:
                Mistake_PA_test[i-1] += 1
            if y_avp_test != y[j]:
                Mistake_Av_Perceptron_test[i-1] += 1

    c += 1

    w_pe_final[i] = w_pe
    w_pa_final[i] = w_pa
    w_avp_final[i] = w_avp
#    print(i, Mistake_Perceptron[i], Mistake_PA[i], w_pe, w_pa)
w_avp_final[-1] = w_avp-u/c

for j in range(len(train)):
    y_pe_test = 1 if np.dot(w_pe_final[-1], train.iloc[j][1:]) >= 0 else -1
    y_pa_test = 1 if np.dot(w_pa_final[-1], train.iloc[j][1:]) >= 0 else -1
    y_avp_test = 1 if np.dot(w_avp_final[-1], train.iloc[j][1:]) >= 0 else -1
    if y_pe_test != y[j]:
        Mistake_Perceptron_test[-1] += 1
    if y_pa_test != y[j]:
        Mistake_PA_test[-1] += 1
    if y_avp_test != y[j]:
        Mistake_Av_Perceptron_test[-1] += 1

# Draw the curve
fig = plt.figure()
p_Perceptron = fig.add_subplot(311)
p_PA = fig.add_subplot(312)
p_Av_Perceptron = fig.add_subplot(313)

p_Perceptron.plot(Mistake_Perceptron)
p_Perceptron.plot(Mistake_PA)
p_PA.plot(Mistake_Perceptron_test)
p_PA.plot(Mistake_PA_test)
p_Av_Perceptron.plot(Mistake_Av_Perceptron)
p_Av_Perceptron.plot(Mistake_Av_Perceptron_test)
plt.show()

