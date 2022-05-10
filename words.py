import pandas as pd
import matplotlib.pyplot as plt
import pprint


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
            # if POS[0] == "nan" and FREQ[0] == "nan":
            # words.append(Words(word, "N/A", "N/A")) # If we want to keep it as N/A
            #     words.append(Words(word, "N/A", str(df['FREQcount'][i])))  # If we want to use FREQcount
            # elif POS[0] == "nan" and FREQ[0] != "nan":
            #     words.append(Words(word, "N/A", FREQ[0]))
            # elif POS[0] != "nan" and FREQ[0] == "nan":
            #     words.append(Words(word, POS[0], str(df['FREQcount'][i])))
            # else:
            if POS[0] == "nan":
                words.append(Words(word, POS[0], str(df['FREQcount'][i])))
            else:
                words.append(Words(word, POS[0], FREQ[0]))
        else:
            for j in range(len(POS)):
                words.append(Words(word, POS[j], FREQ[j]))


def words_without_pos(words):
    f = open("words-without-pos.txt", "w+")
    f.write(f'{"WORD":<100} \t FREQ \n')
    for i in range(0, len(words)):
        if str(words[i].POS) == 'nan':
            f.write(f'{words[i].word:<100} \t {words[i].FREQ} \n')
    f.close()


# currently ignoring nan POS
def total_pos(words):
    total = 0
    for i in range(len(words)):
        if str(words[i].POS) != 'nan':
            total += 1
    print(f"{total} / 74286 POS. Averaging {total / 74286}")
    return total / 74286


# currently ignoring nan POS
def total_pos_reading_from_file():
    total = 0
    num_words = 0
    df = pd.read_excel('SUBTLEX-US-Compressed.xlsx')
    for i in range(len(df['Word'])):
        num_words += 1
        POS = str(df['All_PoS_SUBTLEX'][i]).split(".")
        if len(POS) == 1:
            # if POS[0] == "nan" and FREQ[0] == "nan":
            # words.append(Words(word, "N/A", "N/A")) # If we want to keep it as N/A
            #     words.append(Words(word, "N/A", str(df['FREQcount'][i])))  # If we want to use FREQcount
            # elif POS[0] == "nan" and FREQ[0] != "nan":
            #     words.append(Words(word, "N/A", FREQ[0]))
            # elif POS[0] != "nan" and FREQ[0] == "nan":
            #     words.append(Words(word, POS[0], str(df['FREQcount'][i])))
            # else:
            if POS[0] != "nan":
                total += len(POS)
        else:
            total += len(POS)
    print("Using file reading... ")
    print(f"{total} / 74286 POS. Averaging {total / num_words}")


# Does not include nan values
def frequency_distribution(freq_words):
    frequency = {}
    df = pd.read_excel('SUBTLEX-US-Compressed.xlsx')
    for i in range(len(df['Word'])):
        POS = str(df['All_PoS_SUBTLEX'][i])  # As of now we are treating X.Y separately compared to Y.X
        if POS != 'nan': # remove if statement if we want nan included in this frequency distribution
            frequency[POS] = frequency.get(POS, 0) + 1
    sort_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    f = open("frequency-distribution.txt", "w+")
    for i in sort_frequency:
        # print(f'{i[0]:<100} {i[1]}')
        f.write(f'{i[0]:<100} \t {i[1]} \n')
    f.write(f'\nThe average POS per word is: {freq_words}')
    # pprint.pprint(frequency)
    # pretty_dict_str = pprint.pformat(frequency)

    # f.write(pretty_dict_str)
    f.close()
