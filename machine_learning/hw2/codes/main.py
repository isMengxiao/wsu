# -*- coding: utf-8 -*-

from MySVM import SVM_a, SVM_b, SVM_c
#from KernelizedPerceptron import MyKP


def load_mnist(path, kind='train'):
    import os
    import gzip
    import numpy as np

    labels_path = os.path.join(path,
                    '%s-labels-idx1-ubyte.gz'
                    % kind)
    images_path = os.path.join(path,
                    '%s-images-idx3-ubyte.gz'
                    % kind)

    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8,
                    offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8,
                    offset=16).reshape(len(labels), 784)

    return images, labels


if __name__ == "__main__":
    try:
        images, labels = load_mnist('data/fashion')
        images_test, labels_test = load_mnist('data/fashion', kind='t10k')
        images_validation, labels_validation = \
            images[int(0.8*len(images)):],\
            labels[int(0.8*len(labels)):]
        images_train, labels_train = \
            images[:int(0.8*len(images))],\
            labels[:int(0.8*len(labels))]
    except FileNotFoundError:
        path = input('Data path:')
        images_train, labels_train = load_mnist(path)
        images_test, labels_test = load_mnist(path, kind='t10k')
    except:
        import sys
        print("Unexpected error:", sys.exc_info()[0])
        raise
    print(len(images_train), len(labels_train),
          len(images_validation), len(labels_validation),
          len(images_test), len(labels_test))
    #  Question1_a
    part1_a_maxc, linearSVM = SVM_a(images_train, labels_train,
                        images_validation, labels_validation,
                        images_test, labels_test)

    #  Question1_b
    part1_b_test_accuracy, part1_b_confusion_matrix = SVM_b(part1_a_maxc,
                                    images_train, labels_train,
                                    images_test, labels_test)

    #  Question1_c
    part1_c, degree = SVM_c(part1_a_maxc, linearSVM, images_train, labels_train,
                    images_validation, labels_validation,
                    images_test, labels_test)

    #  Question2
    #part2 = MyKP
