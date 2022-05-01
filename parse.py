import pandas as pd
from words import *


def create_file():
    subtlex = pd.read_excel('SUBTLEX-US frequency list with PoS information.xlsx')
    new_data = subtlex.iloc[:, [0, 12, 13]]
    new_data.to_excel('SUBTLEX-US-Compressed.xlsx', index=True, header=True)