import pandas as pd
import eng_to_ipa as ipa


class Words:
    def __init__(self, word, POS, FREQ):
        self.word = word
        self.POS = POS
        self.FREQ = FREQ


# TODO: Add a clause to automatically adjust the POS if needed for each word
# TODO: Check if we need to change the class to append the POS to the word
# TODO: IPA Conversion in a timely manner, and what to do if IPA conversion doesn't exist

def add_words_to_list(words):
    df = pd.read_excel('SUBTLEX-US-Compressed.xlsx')
    for i in range(len(df['Word'])):
        word = str(df['Word'][i])
        POS = str(df['All_PoS_SUBTLEX'][i]).split(".")
        FREQ = str(df['All_freqs_SUBTLEX'][i]).split(".")
        if len(POS) == 1:
            words.append(Words(word, POS[0], FREQ[0]))
        else:
            for j in range(len(POS)):
                words.append(Words(word, POS[j], FREQ[j]))
