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


# def main():
    # similar = 0
    # sed_ignoring_zerocase = 0
    # sed = 0
    # no_ipa = 0
    # subtlex_dataset
    # subtlex_dataset = []
    # lemmas = []
    # random_sample()
    # print("1")
    # create_file() 
    # print("2")
    # add_words_to_list_from_file(subtlex_dataset)
    # number_of_lemmas(subtlex_dataset, lemmas)
    # print_global()
    # print(len(lemmas))

    # for i in range(0, 500):
    #     print(lemmas[i])
    # update_ipa(subtlex_dataset)
    # print(len(subtlex_dataset))
    # # nan = words_without_pos(subtlex_dataset)
    # # freq = total_pos(subtlex_dataset, nan)
    # # print(freq)
    # # total_pos_reading_from_file()
    # # frequency_distribution(freq)
    # print("3")
    # update_file(subtlex_dataset)
    # create_adjanceylist(subtlex_dataset)
    # create_graph()

def subtlex_file_error(error):
    print("Error: Expected a value of True or False. Got {error}")

def lemma_wordforms_error(error):
    print("Error: Expected a value of 'lemma' or 'wordforms'. Got {error}")

def lemma_size_error(error):
    print("Error: Range specified is out of bounds. Range from 1 - 51228 inclusive was expected, got {error}")

def word_size_error(error):
    print("Error: Range specified is out of bounds. Range from 1 - 74287 inclusive was expected, got {error}")

def edge_list_file_error(error):
    print("Error: File Not Found. Make sure the pathing is correct, and the file is an .adjlist")
        

if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description = 'Parametres')

    parser.add_argument('-sf','--subtlexfile', type = str, metavar = '', help = 'Do you have the IPA Subtlex File (True/False)', required=True)
    parser.add_argument('-al', '--edgelist', type = str, metavar = '', help = 'Name of adjancey list file if you already have one')
    parser.add_argument('-lw', '--lemmawords', type = str, metavar = '', help = 'Specify whether you wanted to use "lemma" or "wordforms" ', required=True)
    parser.add_argument('-size', '--size', type = int, metavar = '', help = "Size of Adjancey List", required=True)
    # parser.add_argument('-r', '--random', type = str, metavar = '', help = "Random Sample (True/False)")

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
    
    elif args.edgelist is not None and ( os.path.isfile(args.edgelist) and os.path.splitext(file_path)[1].lower() == ".adjlist" ):
        edge_list_file_error(args.edgelist)
    
    #Run program here based on arguments
    else:

        subtlex_dataset = []
        lemmas = []
        
        if args.edgelist is not None and os.path.isfile(args.edgelist):
            create_graph(args.edgelist)
        
        elif args.subtlexfile.lower().strip() in ['t', 'true']:
            add_words_to_list_from_file(subtlex_dataset)
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
            # create_graph(filename)
        
        else:
            update_list(args.size, subtlex_dataset)
            update_ipa(subtlex_dataset)
            filename = create_adjanceylist(args.size, subtlex_dataset)
            # create_graph(filename)


    

    

    # if args.subtlexfile:
    #     add_words_to_list_from_file(subtlex_dataset)
    # else:
    #     add_words_to_list(subtlex_dataset)
    
    # print(subtlex_dataset[0].WORD)
    # update_list(args.size, subtlex_dataset)
    
    # update_ipa(subtlex_dataset)


    # # print_global()
    
    # create_adjanceylist(subtlex_dataset)
    # create_graph()
