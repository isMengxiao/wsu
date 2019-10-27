# -*- coding: utf-8 -*-


def MyKP(x_train, y_train, x_validation, y_validation,
         x_test, y_test, degree=2):
    import numpy as np
    import matplotlib.pyplot as plt

    x_train = x_train/(np.zeros(shape=(len(x_train),
                                     int(x_train.size/len(x_train))))+255)
    alpha = np.zeros(shape=(len(x_train), 10))
    training_mistakes = np.zeros(5)
    train_mistake = 0
    validation_mistake = 0
    test_mistake = 0

    for iteration in range(5):
        for i in range(len(x_train)):
            x = x_train[i]
            y = y_train[i]

            y_hat = np.dot((np.dot(x_train, x)+1)**degree, alpha).argmax()

            if y_hat != y:
                training_mistakes[iteration] += 1
                alpha[i, y] += 1
                alpha[i, y_hat] -= 1
        #c = input('plause')

    w = np.dot(alpha.T, x_train)

    train_accuracy =\
    np.sum([pre.argmax() for pre in np.dot(x_train, w.T)]
           == y_train)/len(y_train)
    vali_accuracy =\
    np.sum([pre.argmax() for pre in np.dot(x_validation, w.T)]
           == y_validation)/len(y_validation)
    test_accuracy =\
    np.sum([pre.argmax() for pre in np.dot(x_train, w.T)]
           == y_test)/len(y_test)
    plt.figure(num=2)
    plt.plot(training_mistakes, color="red", label="training mistakes")
    plt.legend()
    plt.xlabel("iteration")
    plt.ylabel("mistakes")
    plt.title("2 The Number of Training Mistakes")
    name = '../part2-'+degree+'./pg'
    plt.savefig(name)
    print("train_accuracy:", train_accuracy*100, "%")
    print("validation_accuracy:",
          vali_accuracy*100, "%")
    print("test_accuracy:", test_accuracy*100, "%")
    print("training mistakes:", training_mistakes)










