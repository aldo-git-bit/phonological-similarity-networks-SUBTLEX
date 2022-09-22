from parse import *
from words import *
from graph import *
from smallworlds import *
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
        

if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description = 'Parametres')

    parser.add_argument('-sf','--subtlexfile', type = bool, metavar = '', help = 'Do you have the IPA Subtlex File (True/False)')
    parser.add_argument('-al', '--edgelist', type = bool, metavar = '', help = 'Already Generated Adjancey/Edge List? (True/False)')
    parser.add_argument('-size', '--size', type = int, metavar = '', help = "Size of Adjancey List")
    parser.add_argument('-r', '--random', type = bool, metavar = '', help = "Random Sample (True/False)")

    args = parser.parse_args()


    # globals.initialize()
    subtlex_dataset = []
    
    # if args.subtlexfile:
    #     add_words_to_list_from_file(subtlex_dataset)
    # else:
    #     add_words_to_list(subtlex_daaset)
    
    test_function(args.size)

    # update_ipa(subtlex_dataset)


    # # print_global()
    
    # create_adjanceylist(subtlex_dataset)



    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     results = executor.map(create_adjanceylist, globals.subtlex_dataset)
    
    # for result in results:
    #     f.write(result)
    #     f.write("\n")
