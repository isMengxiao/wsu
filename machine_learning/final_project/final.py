#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV as gscv
from sklearn.metrics import confusion_matrix
from sklearn.metrics import auc
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression as lgr
from imblearn.over_sampling import SMOTE

import itertools
from sklearn.metrics import precision_recall_curve


def undersample(data):
    y = data.iloc[:, -1]
    fraud = np.array(data[data["Class"] == 1].index)
    normal = np.array(data[data["Class"] == 0].index)
    random = np.array(np.random.choice(normal, len(y[y == 1])))
    under_sample = np.concatenate([fraud, random])
    under_sample = data.iloc[under_sample, :]

    x_undersample = under_sample.iloc[:, under_sample.columns != "Class"]
    y_undersample = under_sample.iloc[:, under_sample.columns == "Class"]
    return x_undersample, y_undersample


def get_data():
    data = pd.read_csv("./data/creditcard.csv")
    y = data.iloc[:, -1]
    x = data.iloc[:, :-1]
    x_train, x_test, y_train, y_test = train_test_split(x, y,
                                            test_size=0.3, random_state=1165)
    x_validation, x_test, y_validation, y_test = train_test_split(x_test,
                                  y_test, test_size=0.333, random_state=1502)

    smote = SMOTE(random_state=321)
    x_train_SMOTE, y_train_SMOTE = smote.fit_sample(x_train, y_train)
    x_train_undersample, y_train_undersample = undersample(data)

    return x_train, x_validation, x_test, x_train_SMOTE, x_train_undersample,\
        y_train, y_validation, y_test, y_train_SMOTE, y_train_undersample


def confusion_matrix_visulization(cm, classes, name):
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(name+'Confusion matrix')
    plt.colorbar()
    marks = np.arange(len(classes))
    plt.xticks(marks, classes, rotation=0)
    plt.yticks(marks, classes)
    thres = cm.max()/2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 fontsize=15,
                 color="white" if cm[i, j] > thres else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predict')
    plt.savefig(name+"_confusion_matrix.jpg")
    plt.close()


x_train, x_validation, x_test, x_train_SMOTE, x_train_undersample,\
y_train, y_validation, y_test, y_train_SMOTE, y_train_undersample = get_data()

params = {'C': [0.0001, 0.001, 0.01, 0.1, 1,
              10, 100, 1000, 10000],
          'penalty': ['l1', 'l2']}

grid_normal = gscv(lgr(), params, cv=10)
grid_undersample = gscv(lgr(), params, cv=10)
grid_SMOTE = gscv(lgr(), params, cv=10)

grid_normal.fit(x_train, y_train)
grid_undersample.fit(x_train_undersample, y_train_undersample)
grid_SMOTE.fit(x_train_SMOTE, y_train_SMOTE)

result_normal = pd.DataFrame(grid_normal.cv_results_)
result_undersample = pd.DataFrame(grid_undersample.cv_results_)
result_SMOTE = pd.DataFrame(grid_SMOTE.cv_results_)

#best1 = np.argmax(result1.mean_test_score.values)

name = ["normal", "undersample", "SMOTE"]
y_normal_predict = grid_normal.predict(x_test)
y_undersample_predict = grid_undersample.predict(x_test)
y_SMOTE_predict = grid_SMOTE.predict(x_test)

y_normal_prob = grid_normal.predict_proba(x_test)
y_undersample_prob = grid_undersample.predict_proba(x_test)
y_SMOTE_prob = grid_SMOTE.predict_proba(x_test)


def test(y_predict, name, y_prob):
    print(name+"test accuracy:", accuracy_score(y_test, y_predict))
    test_matrix = confusion_matrix(y_test, y_predict)
    plt.figure()
    confusion_matrix_visulization(test_matrix, classes=[0, 1], name=name)
    thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    colors = itertools.cycle(['navy', 'turquoise', 'darkorange',
                              'cornflowerblue', 'teal', 'red', 'yellow',
                              'green', 'blue', 'black'])
    plt.figure(figsize=(12, 7))
    j = 1
    for i, color in zip(thresholds, colors):
        y_test_predictions_prob = y_prob[:, 1] > i

        precision, recall, thresholds = precision_recall_curve(y_test,
                                                    y_test_predictions_prob)
        area = auc(recall, precision)

        plt.plot(recall, precision, color=color,
                 label='Threshold: %s, AUC=%0.5f' % (i, area))
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title(name+'Precision-Recall Curve')
        plt.legend(loc="lower left")
    plt.savefig(name+"AUC.jpg")
    plt.close()


test(y_normal_predict, "Original", y_normal_prob)
test(y_undersample_predict, "Undersample", y_undersample_prob)
test(y_SMOTE_predict, "SMOTE", y_SMOTE_prob)




