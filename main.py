from parse import *
from words import *


def main():
    words = []
    create_file()
    add_words_to_list(words)
    print(words[0])
    print(words[1])
    print(words[len(words) - 1])


if __name__ == "__main__":
    main()
