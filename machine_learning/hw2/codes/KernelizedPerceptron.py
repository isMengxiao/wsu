# -*- coding: utf-8 -*-


def MyKP(x_train, y_train, x_validation, y_validation,
         x_test, y_test, degree=2):
    import numpy as np
    x_train = x_train/(np.zeros(shape=(len(x_train),
                                     int(x_train.size/len(x_train))))+255)
    alpha = np.zeros(shape=(len(x_train), 10))
    train_mistake = 0
    validation_mistake = 0
    test_mistake = 0

    for iteration in range(5):
        for i in range(len(x_train)):
            y_hat = 0
            x = x_train[i]
            y = y_train[i]

            y_hat = np.dot((np.dot(x_train, x)+1)**degree, alpha).argmax()

            if y_hat != y:
                alpha[:, y] += 1
                alpha[:, y_hat] -= 1
        print(alpha[1])
        #c = input('plause')

    w = np.dot(alpha.T, x_train)

    for i in range(len(x_train)):
        if np.dot(x_train[i], w.T).argmax() != y_train[i]:
            train_mistake += 1
    for i in range(len(x_validation)):
        if np.dot(x_validation[i], w.T).argmax() != y_validation[i]:
            validation_mistake += 1
    for i in range(len(x_test)):
        if np.dot(x_test[i], w.T).argmax() != y_test[i]:
            test_mistake += 1

    print("train_accuracy:", train_mistake/len(x_train)*100, "%")
    print("validation_accuracy:",
          validation_mistake/len(x_validation)*100, "%")
    print("test_accuracy:", test_mistake/len(x_test)*100, "%")










