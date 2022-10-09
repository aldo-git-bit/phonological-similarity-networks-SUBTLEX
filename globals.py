from parse import *
from words import *
from graph import *
from smallworlds import *

import eng_to_ipa as ipa
import subprocess
import jellyfish


def initialize():
    global subtlex_dataset
    subtlex_dataset = []
    add_words_to_list_from_file(subtlex_dataset)