# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# a. Call the loaded data college.
data = pd.read_csv("College.csv")

# b. Find the median cost of books.
Books_median = data['Books'].median()

# c. Shows the relationship between Books and Top10percent.
fig = plt.figure()
plt1 = fig.add_subplot(111)
plt1.set_title('Relationship between the cost of books and Top 10 percent')

plt.xlabel('Cost of books')
plt.ylabel('Top 10 percent students')

plt1.scatter(data['Books'], data['Top10perc'], c='r', marker='o')

plt.show()

