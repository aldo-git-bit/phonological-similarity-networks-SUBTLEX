from words import *



def create_file():
    subtlex = pd.read_excel('SUBTLEX-US frequency list with PoS information.xlsx')
    new_data = subtlex.iloc[:, [0, 1, 12, 13]]
    new_data.to_excel('SUBTLEX-US-Compressed.xlsx', index=True, header=True)


def update_file(words):
    y = 2
    subtlex = pd.read_excel('SUBTLEX-US-Compressed.xlsx')
    workbook = openpyxl.load_workbook('SUBTLEX-US-Compressed.xlsx')
    worksheet_LM = workbook.worksheets[0]
    worksheet_M = workbook.worksheets[0]

    worksheet_LM.insert_cols(3)
    worksheet_M.insert_cols(4)

    cell_title_IPALM = worksheet_LM.cell(row = 1, column = 3)
    cell_title_IPAM = worksheet_M.cell(row = 1, column = 4)

    cell_title_IPALM.value = "IPA-Conversion-LM"
    cell_title_IPAM.value = "IPA-M"

    for i in words:
        cell_to_write = worksheet_LM.cell(row = y, column = 3)
        if i.IPA[len(i.IPA) - 1] == "*":
            cell_to_write.value = i.IPA_model
        else:
            cell_to_write.value = i.IPA

        cell_to_writeM = worksheet_M.cell(row = y, column = 4)
        cell_to_writeM.value = i.IPA_model
        y += 1
    
    workbook.save('SUBTLEX-US-Compressed.xlsx')

