import pandas as pd
import eng_to_ipa as ipa
import subprocess
import openpyxl

class Words:
    def __init__(self, WORD, IPA, IPA_LIST):
        self.WORD = WORD
        self.IPA = IPA
        self.IPA_LIST = IPA_LIST


def add_words_to_list_from_file(words):
    data = pd.read_excel('SUBTLEX-US-Copy.xlsx')
    df = data.sample(frac = .0013)
    #print(df['Word'])
    # df = pd.read_excel('SUBTLEX-US-Copy.xlsx')
    # df = df.sample(frac = 0.0013)
    # j = 0
    print(df['Word'])

    # Original Code Below
    # for i in range(len(df['Word'])):
    #     WORD = str(df['Word'][i]).strip()
    #     IPA = str(df['IPA'][i]).strip()
    #     IPA_LIST = str(df['IPA-List'][i]).strip().split()
    #     words.append(Words(WORD, IPA, IPA_LIST))


def add_words_to_list(words):
    df = pd.read_excel('SUBTLEX-US-Copy.xlsx')
    for i in range(len(df['Word'])):
        WORD = str(df['Word'][i]).strip()
        IPA = str(ipa.convert(WORD)).strip()
        IPA = IPA.replace("ˈ", "")
        IPA = IPA.replace("ˌ", "")
        if IPA[len(IPA) - 1] == "*":
            IPA = str(subprocess.run(['bash', 'ipa_translator.sh', WORD]))
            with open('ipa_translation.txt') as f:
                lines = f.readlines()
                IPA = lines[0][1:].replace(" ", "")
                IPA = IPA.replace(">", " ")
                IPA = IPA.strip()
                IPA = IPA.strip("\n")
            
       #  if IPA[len(IPA) - 1] == "*":
           #  print(word)
        # subprocess.run(['bash', 'ipa_translator.sh', word])
        # with open('ipa_translation.txt') as f:
        #     lines = f.readlines()
        #     IPA = lines[0][1:].replace(" ", "")
        #     IPA = IPA.replace(">", " ")
        #     IPA = IPA.strip()

        words.append(Words(WORD, IPA, list(IPA)))

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
    df = pd.read_excel('SUBTLEX-US-Copy.xlsx')
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
    df = pd.read_excel('SUBTLEX-US-Copy.xlsx')
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
