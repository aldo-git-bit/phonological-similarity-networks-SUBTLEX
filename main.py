from parse import *
from words import *
import eng_to_ipa as ipa
import subprocess


def main():
    words_pos_separated = []
    # print("1")
    create_file()
    # print("2")
    add_words_to_list(words_pos_separated)
    # # nan = words_without_pos(words_pos_separated)
    # # freq = total_pos(words_pos_separated, nan)
    # # print(freq)
    # # total_pos_reading_from_file()
    # # frequency_distribution(freq)
    # print("3")
    for i in range(0, 500):
        print(f"{words_pos_separated[i].word:<30} \t {words_pos_separated[i].IPA:<100} ")

    # subprocess.run('bash ipa_translator.sh china', shell=True, capture_output=True, text=True)



if __name__ == "__main__":
    main()
