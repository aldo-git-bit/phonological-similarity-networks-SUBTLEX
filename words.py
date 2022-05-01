import pandas as pd


class Words:
    def __init__(self, word, POS, FREQ):
        self.word = word
        self.POS = POS
        self.FREQ = FREQ


class WordList:
    def __init__(self, wordlist):
        self.wordlist = wordlist


def add_words_to_list(words):
    df = pd.read_excel('SUBTLEX-US-Compressed.xlsx')
    for i in range(len(df['Word'])):
        words.append(Words(str(df['Word'][i]), str(df['All_PoS_SUBTLEX'][i]).split("."), str(df['All_freqs_SUBTLEX'][i]).split(".")))



