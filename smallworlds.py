import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def random_sample():
    list_nums = []
    y_axis = []
    df = pd.read_excel("SUBTLEX-US frequency list with PoS information.xlsx")
    df = df.sample(50000)
    for i in df.index:
        list_nums.append(df['FREQcount'][i])
    for i in range(0, 50000):
        y_axis.append(i)
    # df.sort_values(by = ['FREQcount'], ascending = False).sample(500).plot.line()
    plt.show()
    list_nums.sort(reverse=True)
    # print(len(y_axis))
    # print(len(list_nums))
    # plt.plot(list_nums, marker='o')
    plt.scatter(y_axis, list_nums)
    plt.show()

