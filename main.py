from parse import *
from words import *


def main():
    words = []
    create_file()
    add_words_to_list(words)
    for i in range(400, 500):
        print(f"{words[i].word} {words[i].POS} {words[i].FREQ}")


if __name__ == "__main__":
    main()
