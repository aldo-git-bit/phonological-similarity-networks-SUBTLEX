import pandas as pd


class Words:
    def __init__(self, word, POS, FREQ):
        self.word = word
        self.POS = POS
        self.FREQ = FREQ



def add_words_to_list(words):
    df = pd.read_excel('SUBTLEX-US-Compressed.xlsx')
    for i in range(len(df['Word'])):
        if len(str(df['All_PoS_SUBTLEX'][i]).split(".")) == 1:
            words.append(Words(str(df['Word'][i]), str(df['All_PoS_SUBTLEX'][i]), str(df['All_freqs_SUBTLEX'][i])))
        else:
            for j in range(len(str(df['All_PoS_SUBTLEX'][i]).split("."))):
                words.append(Words(str(df['Word'][i]), str(df['All_PoS_SUBTLEX'][i]).split(".")[j], str(df['All_freqs_SUBTLEX'][i]).split(".")[j]))


