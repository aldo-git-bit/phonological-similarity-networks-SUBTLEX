from parse import *
from words import *


def main():
    words = []
    create_file()
    add_words_to_list(words)
    words_without_pos(words)
    total_pos(words)
    total_pos_reading_from_file()


if __name__ == "__main__":
    main()
