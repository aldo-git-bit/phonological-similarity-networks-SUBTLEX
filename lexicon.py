import eng_to_ipa as ipa 
import pyphen 
import networkx as nx
import pandas as pd
import xlsxwriter

class Words:
    def __init__(self, WORD, IPA, IPA_LIST, FREQcount, POS):
        self.WORD = WORD
        self.IPA = IPA
        self.IPA_LIST = IPA_LIST
        self.FREQcount = FREQcount
        self.POS = POS


def update_ipa(words):
    two_character_phonemes = ["oʊ", "ɔɪ", "aɪ", "aʊ"]
    vowels = ["ɑ", "æ", "ə", "ʌ", "ɔ", "a", "aɪ", "aʊ", "ɛ", "e", "ɪ", "i", "o", "ɔ", "ʊ", "u"]

    for i in range(0, len(words)):
        word_1 = words[i].IPA_LIST
        temp_array_word = []
        temp_array_word.append(word_1[0])

        for k in range(1, len(word_1)):
            temp_array_word.append(word_1[k])

            if (word_1[k-1] + word_1[k] == "ər") and (k != len(word_1) - 1) and (word_1[k+1] not in vowels):
                    # print(f"{words[i].WORD}...... {word_1}.....{word_1[k+1]}")
                    temp_array_word.pop()
                    temp_array_word.pop()
                    temp_array_word.append(word_1[k-1] + word_1[k])


            elif (word_1[k-1] + word_1[k] in two_character_phonemes):
                temp_array_word.pop()
                temp_array_word.pop()
                temp_array_word.append(word_1[k-1] + word_1[k])
        
        words[i].IPA_LIST = temp_array_word


def create_lexicon():
    dic = pyphen.Pyphen(lang='en_US')
    words = []
    sections = ["Word", "IPA", "FREQcount", "Dom Pos", "Syllable-ENG-To-IPA", "Syllable-Pyphen","DIFF"]
    graph = nx.read_adjlist("lemma_words19839.adjlist") #for words in adjlist
    df = pd.read_excel('SUBTLEX-US-Copy.xlsx') #get all information in SUBLEX-US that relates to adjlist
    for i in range(len(df['Word'])):
        WORD = str(df['Word'][i]).strip()
        if WORD in graph.nodes():
            IPA = str(df['IPA'][i]).strip()
            IPA_LIST = str(df['IPA-List'][i]).strip().split()
            FREQcount = str(df['FREQcount'][i]).strip()
            POS = str(df['Dom_PoS_SUBTLEX'][i])
            words.append(Words(WORD, IPA, IPA_LIST, FREQcount, POS))
    # update_ipa(words) if IPA is toegether we don't need to do this
    print("Done adding wordS")
    workbook = xlsxwriter.Workbook('Lemma_Words19839-Lexicon.xlsx')
    worksheet = workbook.add_worksheet("Lexicon")
    row = 0
    col = 0
    for i in sections:
        worksheet.write(row, col, i)
        col += 1
    
    row = 1
    col = 0

    for i in words:
        print(i.WORD)
        worksheet.write(row,col, i.WORD)
        worksheet.write(row,col+1,i.IPA)
        worksheet.write(row,col+2,i.FREQcount)
        worksheet.write(row,col+3,i.POS)
        worksheet.write(row,col+4,ipa.syllable_count(i.WORD))
        worksheet.write(row,col+5,len(str(dic.inserted(i.WORD)).split('\u002D')))
        if (ipa.syllable_count(i.WORD) != 0) and (ipa.syllable_count(i.WORD) != len(str(dic.inserted(i.WORD)).split('\u002D'))):
            worksheet.write(row,col+6,"Y")
        row += 1
        col = 0

    workbook.close()

if __name__ == "__main__":
    create_lexicon()
