from words import *
import globals 

def print_global():
    print(len(globals.subtlex_dataset))


def create_file():
    subtlex = pd.read_excel('SUBTLEX-US frequency list with PoS information.xlsx')
    new_data = subtlex.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,12,13]]
    new_data.to_excel('SUBTLEX-US-Copy.xlsx', index=True, header=True)


def update_file(words):
    y = 2
    subtlex = pd.read_excel('SUBTLEX-US-Copy.xlsx')
    workbook = openpyxl.load_workbook('SUBTLEX-US-Copy.xlsx')
    worksheet_LM = workbook.worksheets[0]
    worksheet_M = workbook.worksheets[0]

    worksheet_LM.insert_cols(3)
    worksheet_M.insert_cols(4)

    cell_title_IPALM = worksheet_LM.cell(row = 1, column = 3)
    cell_title_IPAM = worksheet_M.cell(row = 1, column = 4)

    cell_title_IPALM.value = "IPA"
    cell_title_IPAM.value = "IPA-List"

    for i in words:
        cell_to_write = worksheet_LM.cell(row = y, column = 3)
        cell_to_write.value = i.IPA
     

        cell_to_writeM = worksheet_M.cell(row = y, column = 4)
        ipa_list_str = ""
        for i in i.IPA_LIST:
            ipa_list_str = ipa_list_str + i + " "

        cell_to_writeM.value = ipa_list_str
        y += 1
    
    workbook.save('SUBTLEX-US-Copy.xlsx')

