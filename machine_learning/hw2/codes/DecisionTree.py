# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def load_data(path):
    data = pd.read_csv(path, names=['id', 'CT', 'UoCS', 'UoCS2', 'MA',
                                    'SECS', 'BN', 'BC', 'NN', 'M', 'class'],
                       header=None)
    #x, y = data[:, 1:-1], data[:, -1]
    data = data.drop('id', axis=1)
    data_train, data_test = train_test_split(data, test_size=0.3)
    data_validation, data_test = train_test_split(data_test, test_size=0.333)

    return data_train, data_validation, data_test


def entropy(col):
    elements, counts = np.unique(col, return_counts=True)
    entropys = np.sum([(-counts[i]/np.sum(counts))
                       *np.log2(counts[i]/np.sum(counts))
                       for i in range(len(elements))])
    return entropys


def IG(data, name1, name2):
    total_entropys = entropy(data[name2])

    elements, counts = np.unique(data[name1], return_counts=True)

    weight = np.sum([(counts[i]/np.sum(counts))*
            entropy(data.where(data[name1] == elements[i]).dropna()[name2])
                     for i in range(len(elements))])

    Infor_Gain = total_entropys - weight
    return Infor_Gain


def ID3_tree(subdata, data, features, target="class", parent_node=None):
    if len(data) == 0:
        return np.unique(data[target])[
            np.argmax(np.unique(data[target], return_counts=True)[1])]

    if len(np.unique(data[target])) <= 1:
        return np.unique(data[target])[0]

    if len(features) == 0:
        return parent_node

    else:
        parent_node = np.unique(subdata[target])[np.argmax(np.unique(
            subdata[target], return_counts=True)[1])]

        items = [IG(subdata, feature, target) for feature in features]
        best_feature = features[np.argmax(items)]

        tree = {best_feature: {}}

        features = [i for i in features if i != best_feature]

        for value in np.unique(subdata[best_feature]):
            sub_data = subdata.where(subdata[best_feature] == value).dropna()
            subtree = ID3_tree(sub_data, data, features, target, parent_node)

            tree[best_feature][value] = subtree

        return tree


def predict(groups, tree, default=4.0):
    for key in list(groups.keys()):
        if key in list(tree.keys()):
            try:
                result = tree[key][groups[key]]
            except:
                return default
            result = tree[key][groups[key]]
            if isinstance(result, dict):
                return predict(groups, result)
            else:
                return result

def test(data, data_name, tree):
    groups = data.iloc[:, :-1].to_dict(orient="records")
    prediction = pd.DataFrame(columns=["predict"])
    for i in range(len(data)):
        prediction.loc[i, "predict"] = predict(groups[i], tree, 4.0)
    print(prediction)
    print("data class:", data["class"])
    print(data_name, 'Accuracy is:',
          (np.sum(prediction["predict"] == data["class"])/len(data)))

if __name__ == "__main__":
    data_train, data_validation, data_test =\
        load_data('data/breast-cancer-wisconsin.data')
    tree = ID3_tree(data_train, data_train, data_train.columns[:-1])
    print(tree)
    test(data_validation, 'validation', tree)
    test(data_test, 'test', tree)
