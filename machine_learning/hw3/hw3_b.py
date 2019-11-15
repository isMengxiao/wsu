# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from torch import tensor
import torch
import matplotlib as mpl
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
import math


def get_data():
    train_data = pd.read_csv('./data/fashion-mnist_train.csv')
    test_data = pd.read_csv('./data/fashion-mnist_test.csv')
    x_train = train_data[train_data.columns[1:]].values
    y_train = train_data.label.values
    x_test = test_data[test_data.columns[1:]].values
    y_test = test_data.label.values
    return map(tensor, (x_train, y_train, x_test, y_test))


class FashionMnistNet(nn.Module):
    # Based on Lecunn's Lenet architecture
    def __init__(self):
        super(FashionMnistNet, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 8, 5, 2, 2),
            nn.ReLU(),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(8, 16, 3, 2, 1),
            nn.ReLU(),
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(16, 32, 3, 2, 1),
            nn.ReLU(),
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(32, 32, 3, 2, 1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.fc1 = nn.Linear(32*1*1, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = x.view(-1, self.num_flat_features(x))
        x = self.fc1(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


def train(model, lr, epochs, bs, opt, x_train, y_train, x_test, y_test, name):
    train_n, train_m = x_train.shape
    test_n, test_m = x_test.shape
    loss_func = F.cross_entropy # loss function
    accuracy_vals = []
    print(name)
    for epoch in range(epochs):
        model.train()
        for i in range((train_n-1)//bs + 1):
            start_i = i*bs
            end_i = start_i+bs
            xb = x_train[start_i:end_i].reshape(bs, 1, 28, 28)
            yb = y_train[start_i:end_i]
            loss = loss_func(model.forward(xb), yb)
            loss.backward()
            opt.step()
            opt.zero_grad()
        model.eval()
        with torch.no_grad():
            total_loss, accuracy = 0., 0.
            validation_size = int(test_n/10)
            for i in range(test_n):
                x = x_test[i].reshape(1, 1, 28, 28)
                y = y_test[i]
                pred = model.forward(x)
                accuracy += (torch.argmax(pred) == y).float()
            print("Accuracy: ", (accuracy*100/test_n).item())
            accuracy_vals.append((accuracy*100/test_n).item())
    plt.figure(num=1)
    plt.plot(accuracy_vals, label="accuracy")
    plt.legend()
    plt.xlabel("Number of epochs")
    plt.ylabel("Accuracy")
    plt.title(name)
    plt.savefig(name+'.jpg')
    plt.close()


def normalize(x, m, s):
    return (x-m)/s


def find_lr(net, loss_func):
    final_value = 10.0
    beta = 0.98
    bs = 32
    init_value = 1e-8
    num = (train_n-1)//bs + 1 # num of batches
    mult = (final_value/init_value) ** (1/num)
    lr = init_value
    optimizer = optim.SGD(net.parameters(), lr=lr)
    avg_loss = 0.
    best_loss = 0.
    batch_num = 0.
    losses = []
    lrs = []
    log_lrs = []
    for i in range((train_n-1)//bs + 1):
        batch_num += 1
        start_i = i*bs
        end_i = start_i+bs
        xb = x_train[start_i:end_i].reshape(bs, 1, 28, 28)
        yb = y_train[start_i:end_i]
        optimizer.zero_grad()
        outputs = net.forward(xb)
        loss = loss_func(outputs, yb)
        # Compute the smoothed loss
        avg_loss = beta * avg_loss + (1-beta) *loss.item()
        smoothed_loss = avg_loss / (1 - beta**batch_num)
        # Stop if the loss is exploding
        if batch_num > 1 and smoothed_loss > 4 * best_loss:
            return log_lrs, losses
        # Record the best loss
        if smoothed_loss < best_loss or batch_num == 1:
            best_loss = smoothed_loss
        # Store the values
        losses.append(smoothed_loss)
        log_lrs.append(lr)
        # Do the SGD step
        loss.backward()
        optimizer.step()
        # Update the lr for the next step
        lr *= mult
        optimizer.param_groups[0]['lr'] = lr
    return log_lrs, losses


if __name__ == "__main__":
    x_train, y_train, x_test, y_test = get_data()
    x_train, x_test = x_train.float(), x_test.float()
    train_n, train_m = x_train.shape
    test_n, test_m = x_test.shape
    n_cls = y_train.max()+1

    model = FashionMnistNet()  # Creating a model
    lr = 0.05  # learning rate
    epochs = 10  # number of epochs
    bs = 32  # batch size
    opt = optim.Adam(model.parameters(), lr=lr)
    train(model, lr, epochs, bs, opt, x_train, y_train,
          x_test, y_test, "First Train:")

    train_mean, train_std = x_train.mean(), x_train.std()
    x_train = normalize(x_train, train_mean, train_std)
    x_test = normalize(x_test, train_mean, train_std)
    model_norm = FashionMnistNet()
    opt_norm = optim.SGD(model_norm.parameters(), lr=lr)
    train(model_norm, lr, epochs, bs, opt_norm, x_train, y_train,
          x_test, y_test, "Second train with normalization:")

    model_lrfinder = FashionMnistNet()
    loss_func = F.cross_entropy
    log_lrs, losses = find_lr(model_lrfinder, loss_func)
    lr = log_lrs[losses.index(min(losses))]
    print(lr)

    train(model_lrfinder, lr, epochs, bs, opt_norm,
          x_train, y_train, x_test, y_test, "Third train with better lr:")
