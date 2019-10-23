# -*- coding: utf-8 -*-

from main import load_mnist
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from KernelizedPerceptron import MyKP



if __name__ == '__main__':
    images, labels = load_mnist('data/fashion')
    x_test, y_test = load_mnist('data/fashion', kind='t10k')
    x_train, x_validation, y_train, y_validation =\
        train_test_split(images, labels, test_size=0.2)
    MyKP(x_train, y_train, x_validation, y_validation, x_test, y_test)
