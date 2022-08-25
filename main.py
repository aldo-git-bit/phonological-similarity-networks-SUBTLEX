from parse import *
from words import *
from graph import *
from smallworlds import *

import eng_to_ipa as ipa
import subprocess
import jellyfish


def main():
    # similar = 0
    # sed_ignoring_zerocase = 0
    # sed = 0
    # no_ipa = 0

    words_pos_separated = []
    # random_sample()
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
    # update_file(words_pos_separated)
    create_adjanceylist(words_pos_separated)
    create_graph()
    # subprocess.run('bash ipa_translator.sh china', shell=True, capture_output=True, text=True)

if __name__ == "__main__":
    main()
