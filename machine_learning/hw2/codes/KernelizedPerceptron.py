# -*- coding: utf-8 -*-


def MyKP(x_train, y_train, x_test, y_test, degree=2):
    import numpy as np
    alpha = np.zeros(shape=(10, 784))
    train_mistake = np.zeros(5)
    validation_mistake = np.zeros(5)
    test_mistake = np.zeros(5)

    for iteration in range(5):
        for i in range(len(x_train)):
            y_hat = 0
            x = x_train[i]
            y = y_train[i]

            y_hat = np.dot(alpha, (np.dot(x_train, x)+1)**degree).argmax()

            if y_hat != y:
                y_hat = int(y_hat)








