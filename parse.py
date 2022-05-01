from words import *

# TODO: Expand columns to have data be nicely formtted when opening the excel file


def create_file():
    subtlex = pd.read_excel('SUBTLEX-US frequency list with PoS information.xlsx')
    new_data = subtlex.iloc[:, [0, 12, 13]]
    new_data.to_excel('SUBTLEX-US-Compressed.xlsx', index=True, header=True)