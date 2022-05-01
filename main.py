from parse import *
from words import *


def main():
    words = []
    create_file()
    add_words_to_list(words)
    print(words[0].word, words[0].POS[0], words[0].FREQ[0])


if __name__ == "__main__":
    main()
