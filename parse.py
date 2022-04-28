import pandas as pd


def random_function():
    subtlex = pd.read_excel('SUBTLEX-US frequency list with PoS information.xlsx', engine='openpyxl')
    print(subtlex)