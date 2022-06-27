import pandas as pd
import eng_to_ipa as ipa
import subprocess
import openpyxl

class Words:
    def __init__(self, WORD, IPA, IPA_model):
        self.WORD = WORD
        self.IPA = IPA
        self.IPA_model = IPA_model


# TODO: Think about what we want to do for words with N/A ratings. Currently displayed as nan but changed to N/A
"""
For words without values in the "All_freqs_SUBTLEX" field, we could grab the number from FREQcount as well, but 
we will be left without a Part of Speech, and we are unsure what the relationship between count and POS would be 
"""

# TODO: Add a clause to automatically adjust the POS if needed for each word
""" 
We'll have to check with an if statement for the word if we want to automate this. 
e.g if word == "horsefly" -> words.append(word, "Noun", FREQ[0])

"""


# TODO: Check if we need to change the class to append the POS to the word
# TODO: IPA Conversion in a timely manner, and what to do if IPA conversion doesn't exist

def add_words_to_list(words):
    j = 0
    df = pd.read_excel('SUBTLEX-US-Compressed.xlsx')

    for i in range(len(df['Word'])):
        if j == 10:
            break
        
        WORD = str(df['Word'][i]).strip()
        IPA = str(ipa.convert(WORD)).strip()
        IPA = IPA.replace("ˈ", "")
        IPA = IPA.replace("ˌ", "")


        IPA_model = str(subprocess.run(['bash', 'ipa_translator.sh', WORD]))
        with open('ipa_translation.txt') as f:
            lines = f.readlines()
            IPA_model = lines[0][1:].replace(" ", "")
            IPA_model = IPA_model.replace(">", " ")
            IPA_model = IPA_model.strip()
            IPA_model = IPA_model.strip("\n")
            
       #  if IPA[len(IPA) - 1] == "*":
           #  print(word)
        # subprocess.run(['bash', 'ipa_translator.sh', word])
        # with open('ipa_translation.txt') as f:
        #     lines = f.readlines()
        #     IPA = lines[0][1:].replace(" ", "")
        #     IPA = IPA.replace(">", " ")
        #     IPA = IPA.strip()

        words.append(Words(WORD, IPA, IPA_model))
        j += 1


def words_without_pos(words):
    total = 0
    f = open("words-without-pos.txt", "w+")
    f.write(f'{"WORD":<100} \t FREQ \n')
    for i in range(0, len(words)):
        if str(words[i].POS) == 'nan':
            f.write(f'{words[i].word:<100} \t {words[i].FREQ} \n')
            total += 1
    f.close()
    return total


# currently ignoring nan POS
def total_pos(words, total_nan):
    total = 0
    for i in range(len(words)):
        if str(words[i].POS) != 'nan':
            total += 1
    print(f"{total} / 74095 POS. Averaging {(total / (74286 - total_nan))}")
    return total / (74286 - total_nan)


# currently ignoring nan POS
def total_pos_reading_from_file():
    total = 0
    num_words = 0
    df = pd.read_excel('SUBTLEX-US-Compressed.xlsx')
    for i in range(len(df['Word'])):
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
                num_words += 1
                total += len(POS)
        else:
            total += len(POS)
            num_words += 1
    print("Using file reading... ")
    print(f"{total} / {num_words} POS. Averaging {total / num_words}")


# Does not include nan values
def frequency_distribution(freq_words):
    frequency = {}
    df = pd.read_excel('SUBTLEX-US-Compressed.xlsx')
    for i in range(len(df['Word'])):
        POS = str(df['All_PoS_SUBTLEX'][i])  # As of now we are treating X.Y separately compared to Y.X
        if POS != 'nan':  # remove if statement if we want nan included in this frequency distribution
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
