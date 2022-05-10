from parse import *
from words import *


def main():
    words_pos_seperated = []
    create_file()
    add_words_to_list(words_pos_seperated)
    words_without_pos(words_pos_seperated)
    freq = total_pos(words_pos_seperated)
    print(freq)
    total_pos_reading_from_file()
    frequency_distribution(freq)


if __name__ == "__main__":
    main()
