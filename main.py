from parse import *
from words import *


def main():
    words = []
    create_file()
    add_words_to_list(words)
    words_without_pos(words)


if __name__ == "__main__":
    main()
