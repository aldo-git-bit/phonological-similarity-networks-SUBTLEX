from parse import *
from words import *
from graph import *
from smallworlds import *
import os
import globals
import argparse
import eng_to_ipa as ipa
import subprocess
import jellyfish
import concurrent.futures


def subtlex_file_error(error):
    print("Error: Expected a value of True or False. Got {error}")

def lemma_wordforms_error(error):
    print("Error: Expected a value of 'lemma' or 'wordforms'. Got {error}")

def lemma_size_error(error):
    print("Error: Range specified is out of bounds. Range from 1 - 51228 inclusive was expected, got {error}")

def word_size_error(error):
    print("Error: Range specified is out of bounds. Range from 1 - 74287 inclusive was expected, got {error}")


if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description = 'Parametres')

    parser.add_argument('-sf','--subtlexfile', type = str, metavar = '', help = 'Do you have the IPA Subtlex File (True/False)', required=True)
    parser.add_argument('-lw', '--lemmawords', type = str, metavar = '', help = 'Specify whether you wanted to use "lemma" or "wordforms" ', required=True)
    parser.add_argument('-size', '--size', type = int, metavar = '', help = "Size of Adjancey List", required=True)
    args = parser.parse_args()
    
    
    # Check conditions 
    if args.subtlexfile.lower().strip() not in ['f', 'false', 't', 'true']:
        subtlex_file_error(args.subtlexfile)
    
    elif args.lemmawords.lower().strip() not in ['lemma', 'wordforms']:
        lemma_wordforms_error(args.lemmawords)
    
    elif args.lemmawords.lower().strip() == 'lemma' and (args.size <= 0 or args.size >= 51229 ):
        lemma_size_error(args.size)
    
    elif args.lemmawords.lower().strip() == 'wordforms' and (args.size <= 0 or args.size >= 74288 ):
        word_size_error(args.size)
    
    
    #Run program here based on arguments
    else:

        subtlex_dataset = []
        lemmas = []
    
        if args.edgelist is not None and os.path.isfile(args.edgelist):
            create_graph(args.edgelist)
        
        elif args.subtlexfile.lower().strip() in ['t', 'true']:
            add_words_to_list_from_file(subtlex_dataset)
            print(f"THIS IS LEN OF DATASET {len(subtlex_dataset)}")
        else:
            create_file()
            add_words_to_list(subtlex_dataset)
            update_file()
    
        if args.lemmawords.lower().strip() =='lemma':
            number_of_lemmas(subtlex_dataset, lemmas)
            print(f"Number of m lemmas {len(lemmas)}")
            update_list(args.size, lemmas)
            update_ipa(lemmas)
            filename = create_adjanceylist_lemma(args.size, lemmas)
            
        
        else:
            update_list(args.size, subtlex_dataset)
            update_ipa(subtlex_dataset)
            filename = create_adjanceylist(args.size, subtlex_dataset)
            

