import eng_to_ipa as ipa
import pandas as pd 

class Words:
    def __init__(self, WORD, IPA, IPA_LIST, FREQ):
        self.WORD = WORD
        self.IPA = IPA
        self.IPA_LIST = IPA_LIST
        self.FREQ = FREQ
        self.NEW_IPA_LIST = ""
        self.LENGTH = ""




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
        
        words[i].NEW_IPA_LIST = temp_array_word



def get_length(words):
    for i in range(0, len(words)):
        words[i].LENGTH = len(words[i].IPA_LIST)


def add_words_to_list_from_file(words):
    df = pd.read_excel('words_giant.xlsx')
    for i in range(len(df['word'])):
        WORD = str(df['word'][i]).strip()
        IPA = str(df['IPA'][i]).strip()
        IPA_LIST = str(df['IPA_LIST'][i]).strip().split()
        FREQcount = int(df['frequency'][i])
        words.append(Words(WORD, IPA, IPA_LIST, FREQcount))


def update_excel_with_ipa(words):
    df = pd.read_excel('words_giant.xlsx')
    ipa_column = [word.IPA for word in words]
    ipa_list_column = [','.join(word.NEW_IPA_LIST) for word in words] 
    length_column = [word.LENGTH for word in words]
    df['NEW_IPA_LIST'] = ipa_list_column
    df['Word_Length'] = length_column

    df.to_excel('words_giant_updated.xlsx', index=False)  


new_list = []
add_words_to_list_from_file(new_list)
update_ipa(new_list)
get_length(new_list)
update_excel_with_ipa(new_list)




