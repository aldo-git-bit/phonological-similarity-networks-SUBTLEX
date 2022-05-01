import pandas as pd
import eng_to_ipa as ipa


class Words:
    def __init__(self, word, POS, FREQ):
        self.word = word
        self.POS = POS
        self.FREQ = FREQ


# TODO: Think about what we want to do for words with N/A ratings. Currently displayed as nan but changed to N/A
"""
For words without values in the "All_freqs_SUBTLEX" field, we could grab the number from FREQcount as well, but 
we will be left without a Part of Speech, and we are unsure what the relationship between count and POS would be 
"""

# TODO: Add a clause to automatically adjust the POS if needed for each word
""" 
We'll have to check with an if statement for the word if we want to automate this. 
e.g if word == "horsefly" -> words.append(word, "Noun", FREQ[0]

"""


# TODO: Check if we need to change the class to append the POS to the word
# TODO: IPA Conversion in a timely manner, and what to do if IPA conversion doesn't exist

def add_words_to_list(words):
    df = pd.read_excel('SUBTLEX-US-Compressed.xlsx')
    for i in range(len(df['Word'])):
        word = str(df['Word'][i])
        POS = str(df['All_PoS_SUBTLEX'][i]).split(".")
        FREQ = str(df['All_freqs_SUBTLEX'][i]).split(".")
        if len(POS) == 1:
            if POS[0] == "nan" and FREQ[0] == "nan":
                # words.append(Words(word, "N/A", "N/A")) # If we want to keep it as N/A
                words.append(Words(word, "N/A", str(df['FREQcount'][i])))  # If we want to use FREQcount
            elif POS[0] == "nan" and FREQ[0] != "nan":
                words.append(Words(word, "N/A", FREQ[0]))
            elif POS[0] != "nan" and FREQ[0] == "nan":
                words.append(Words(word, POS[0], str(df['FREQcount'][i])))
            else:
                words.append(Words(word, POS[0], FREQ[0]))
        else:
            for j in range(len(POS)):
                words.append(Words(word, POS[j], FREQ[j]))
