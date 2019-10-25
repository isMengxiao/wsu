# -*- coding: utf-8 -*-
import numpy as np

global OriginTree
global CopyTree


def TestCompare(tree, new_tree):
    from DecisionTree import load_data, predict
    data_train, data, data_test = \
        load_data('data/breast-cancer-wisconsin.data')
    groups1 = data.iloc[:, :-1].to_dict(orient="records")
    groups2 = data.iloc[:, :-1].to_dict(orient="records")
    prediction1 = np.zeros(len(data))
    prediction2 = np.zeros(len(data))
    for i in range(len(data)):
        prediction1[i] = predict(groups1[i], tree, 4.0)
        prediction2[i] = predict(groups2[i], tree, 4.0)
    old_accurate = np.sum(prediction1 == data["class"])
    new_accurate = np.sum(prediction2 == data["class"])
    if old_accurate < new_accurate:
        return True
    else:
        return False


def FindEnd(tree, p_node=None, pp_node=None, ppp_node=None):
    global OriginTree
    global CopyTree
    keys = 0
    if type(tree) != float:
        keys = [key for key in tree.keys()]
    else:
        pppkeys = [key for key in ppp_node.keys()]
        if ppp_node[pppkeys[0]] != float:
            ppkeys = [key for key in ppp_node[pppkeys[0]].keys()]
            #print(pppkeys)
            print(ppp_node)
            s = np.unique([i for i in ppp_node[pppkeys[0]][ppkeys[0]].values()],
                      return_counts=True)
            ppp_node[pppkeys[0]] = s[0][s[1].argmax()]
            if TestCompare(OriginTree, CopyTree):
                OriginTree = CopyTree

    if keys:
        ppp_node = pp_node
        pp_node = p_node
        p_node = tree
        for i in keys:
            FindEnd(tree[i], p_node, pp_node, ppp_node)


if __name__ == '__main__':
    with open('MyDecisionTree.txt') as file:
        dict = file.readline()

    exec("tree="+dict)
    OriginTree = tree
    CopyTree = OriginTree.copy()
    FindEnd(CopyTree)
    #print(OriginTree)
    #new_tree = Prune(tree)
