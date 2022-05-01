from parse import *
from words import *


def main():
    words = []
    create_file()
    add_words_to_list(words)
    print(words[4].word, words[4].POS, words[4].FREQ)
    print(words[11].word, words[11].POS, words[11].FREQ)


if __name__ == "__main__":
    main()
