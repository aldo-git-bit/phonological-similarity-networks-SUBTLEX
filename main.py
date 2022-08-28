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

    subtlex_dataset = []
    # random_sample()
    # print("1")
    create_file()
    # print("2")
    add_words_to_list(subtlex_dataset)
    # print(len(subtlex_dataset))
    # # nan = words_without_pos(subtlex_dataset)
    # # freq = total_pos(subtlex_dataset, nan)
    # # print(freq)
    # # total_pos_reading_from_file()
    # # frequency_distribution(freq)
    # print("3")
    update_file(subtlex_dataset)
    # create_adjanceylist(subtlex_dataset)
    # create_graph()

if __name__ == "__main__":
    main()
