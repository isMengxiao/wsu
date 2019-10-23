# -*- coding: utf-8 -*-


def SVM_a(x_train, y_train, x_validation, y_validation, x_test, y_test):
    from sklearn.svm import LinearSVC
    import numpy as np
    import matplotlib.pyplot as plt
    iteration = []
    train_accuracy = np.zeros(len(range(-4, 5)))
    validation_accuracy = np.zeros(len(range(-4, 5)))
    test_accuracy = np.zeros(len(range(-4, 5)))
    for i in np.arange(-4, 5, dtype=float):
        MyC = 10**i
        iteration.append(str(MyC))
        clf = LinearSVC(C=MyC)
        clf.fit(x_train, y_train)
        index = int(i+4)
        train_accuracy[index] = np.sum(y_train == clf.predict(x_train))
        validation_accuracy[index] = np.sum(y_validation ==
                                          clf.predict(x_validation))
        test_accuracy[index] = np.sum(y_test == clf.predict(x_test))

    plt.figure(num=1)
    plt.plot(train_accuracy/len(y_train), color="red",
             label="train_accuracy")
    plt.plot(validation_accuracy/len(y_validation),
             color="green", label="validation_accuracy")
    plt.plot(test_accuracy/len(y_test), color="blue",
             label="test_accuracy")
    plt.xticks(range(9), iteration)
    plt.legend()
    plt.xlabel("C-value")
    plt.ylabel("Accuracy")
    plt.title("1-a Accuracy curve")
    plt.savefig('./part1_a.jpg')
    #plt.show()
    best = int(validation_accuracy.argmax()-4)
    Best_C = 10**best
    Best_element = [train_accuracy[best]/len(y_train),
                    validation_accuracy[best]/len(y_validation),
                    test_accuracy[best]/len(y_test)]
    print('1-a-Best C:', Best_C)
    return Best_C, Best_element


def SVM_b(MyC, x_train, y_train, x_test, y_test):
    from sklearn.svm import LinearSVC
    from sklearn import metrics
    import numpy as np
    clf = LinearSVC(C=MyC)
    clf.fit(x_train, y_train)
    y_predict = clf.predict(x_test)
    test_accuracy = np.sum(y_test == y_predict)
    cm_test = metrics.confusion_matrix(y_test, y_predict)
    print('1-b-testing accuracy:', test_accuracy/len(y_test))
    print('1-b-confusion matrix:', cm_test)
    return test_accuracy, cm_test


def SVM_c(MyC, linearSVM, x_train, y_train, x_validation, y_validation,
          x_test, y_test):
    from sklearn.svm import SVC
    import numpy as np
    degrees = [2, 3, 4]
    train_accuracy = np.zeros(4)
    train_accuracy[0] = linearSVM[0]
    validation_accuracy = np.zeros(4)
    validation_accuracy[0] = linearSVM[1]
    test_accuracy = np.zeros(4)
    test_accuracy[0] = linearSVM[2]
    SV_number = [0]
    for i in degrees:
        clf = SVC(kernel='poly', degree=i, C=MyC, gamma='auto')
        clf.fit(x_train, y_train)
        train_accuracy[i-1] = np.sum(y_train ==
                                     clf.predict(x_train))/len(y_train)
        validation_accuracy[i-1] = np.sum(y_validation ==
                                clf.predict(x_validation))/len(y_validation)
        test_accuracy[i-1] = np.sum(y_test == clf.predict(x_test))/len(y_test)
        SV_number.append(clf.n_support_)

    result = {'train_accuracy': train_accuracy,
              'validation_accuracy': validation_accuracy,
              'test_accuracy': test_accuracy,
              'Number of Support Vectors': SV_number}
    print('1-c-result', result)
    print('1-c-degree:', test_accuracy.argmax()+1)
    return result, test_accuracy.argmax()+1

