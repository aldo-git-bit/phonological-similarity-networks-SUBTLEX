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

if __name__ == "__main__":  
    dataset = []
    create_file()
    add_words_to_list(dataset)
    update_file(dataset)
    update_ipa(dataset)
    filename = create_adjanceylist(19839,dataset)

    
    # #Run program here based on arguments
    # else:

    #     subtlex_dataset = []
    #     lemmas = []
    
    #     if args.edgelist is not None and os.path.isfile(args.edgelist):
    #         create_graph(args.edgelist)
        
    #     elif args.subtlexfile.lower().strip() in ['t', 'true']:
    #         add_words_to_list_from_file(subtlex_dataset)
    #         print(f"THIS IS LEN OF DATASET {len(subtlex_dataset)}")
    #     else:
    #         create_file()
    #         add_words_to_list(subtlex_dataset)
    #         update_file()
    
    #     if args.lemmawords.lower().strip() =='lemma':
    #         number_of_lemmas(subtlex_dataset, lemmas)
    #         print(f"Number of m lemmas {len(lemmas)}")
    #         update_list(args.size, lemmas)
    #         update_ipa(lemmas)
    #         filename = create_adjanceylist_lemma(args.size, lemmas)
    #         # create_graph(filename)
        
    #     else:
    #         update_list(args.size, subtlex_dataset)
    #         update_ipa(subtlex_dataset)
    #         filename = create_adjanceylist(args.size, subtlex_dataset)
    #         # create_graph(filename)


    

    

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
