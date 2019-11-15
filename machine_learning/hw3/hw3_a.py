# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


def load_data(path):
    import os
    kind = ["train", "test"]
    name_list = []
    with open(os.path.join(path, 'stoplist.txt'), 'r') as words:
        lines = words.readlines()
    for line in lines:
        if line not in name_list:
            name_list.append(line[:-1])
    data = []
    label = []
    for k in kind:
        data_path = os.path.join(path, '%sdata.txt' % k)
        label_path = os.path.join(path, '%slabels.txt' % k)
        with open(data_path, 'r') as datas:
            lines = datas.readlines()
            matrix = np.zeros(shape=(len(lines), len(name_list)))
            data.append(pd.DataFrame(matrix, columns=name_list))
            num = 0
            for line in lines:
                line = line[:-1]
                words = line.split(' ')
                for word in words:
                    if word in name_list:
                        data[kind.index(k)].iloc[num][word] += 1
                num += 1
        with open(label_path, 'r') as labels:
            lines = labels.readlines()
            label.append(np.zeros(len(lines)))
            num = 0
            for line in lines:
                label[kind.index(k)][num] = line
                num += 1
    data[0]["classes"] = label[0]
    data[1]["classes"] = label[1]
    return data[0], data[1]


def NaiveBayes(data_train, data_test, data_name):
    right = 0
    print("length:", len(data_train))
    p1 = (data_train.classes.sum()+1)/(len(data_train)+2)
    p0 = (len(data_train)-data_train.classes.sum()+1)/(len(data_train)+2)
    for i in range(len(data_test)):
        x = data_test.iloc[i][:-1]
        y = data_test.iloc[i][-1]
        p_true = p1
        p_false = p0
        for word in data_train.keys():
            if word != "classes":
                # print(word)
                # print(word)
                # print(data_train[data_train["classes"] > 0].sum()[word])
                # print(data_train[data_train["classes"] > 0].count()[word])
                pu1_1 = data_train[data_train["classes"] == 1].sum()[word]
                pu1_n = data_train[data_train["classes"] == 1].count()[word]
                pu1 = pu1_1/pu1_n
                pu0 = data_train[data_train["classes"] == 0].sum()[word]/\
                    data_train[data_train["classes"] == 0].count()[word]
                if pu1:
                    p_true = p_true * pu1
                if pu0:
                    p_false = p_false * pu0
        #print("p=1", p_true)
        if max(p_true, p_false) == p_true:
            y_hat = 1
        else:
            y_hat = 0
        if y_hat == y:
            right += 1
    print("%s accuracy:" % data_name, right/len(data_test))

if __name__ == "__main__":
    path = "./data"
    data_train, data_test = load_data(path)
    #NaiveBayes(data_train, data_train, "train")
    NaiveBayes(data_train, data_test, "test")

