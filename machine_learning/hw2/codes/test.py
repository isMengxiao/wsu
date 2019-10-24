# -*- coding: utf-8 -*-


def FindEnd(tree, p_node=None):
    keys = 0
    if type(tree) != float:
        keys = [key for key in tree.keys()]
    else:
        print(tree)
    if keys:
        for i in keys:
            p_node = tree
            FindEnd(tree[i], p_node)


if __name__ == '__main__':
    with open('MyDecisionTree.txt') as file:
        dict = file.readline()

    exec("tree="+dict)
    FindEnd(tree)
