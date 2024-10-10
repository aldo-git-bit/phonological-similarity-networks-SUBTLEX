# Open access network science: Phonological similarity networks from the SUBTLEX-US lexicon

We constructed several phonological similarity networks (neighbors differ in exactly one consonant/vowel phoneme) using words from a lexicon based on the SUBTLEX-US English corpus, distinguishing networks by size and lemma vs. wordform representations. The resulting networks are shown to exhibit many familiar characteristics, including small world properties and robustness to node removal, regardless of network size and representation type. We also validated the SUBTLEX phonological networks by showing that they exhibit contrasts in degree and clustering coefficient comparable to the same contrasts found in eight prior studies. 


## Acknowledgement
The files with the commit message "Adding model created by LonelyRider-cs/LING4100_project" were created by github user [@LonelyRider-cs](https://github.com/LonelyRider-cs). Their model was used to generate the IPA for words when eng-to-ipa was unable to generate an IPA for a given word. 

More acknowledgements are as followed: 

**OpenNMT**
```
@inproceedings{opennmt,
    author  = {Guillaume Klein and
               Yoon Kim and
               Yuntian Deng and
               Jean Senellart and
               Alexander M. Rush},
  title     = {OpenNMT: Open-Source Toolkit for Neural Machine Translation},
  booktitle = {Proc. ACL},
  year      = {2017},
  url       = {https://doi.org/10.18653/v1/P17-4012},
  doi       = {10.18653/v1/P17-4012}
}
```
**eng-to-ipa**
```
@inproceedings{English-to-IPA,
    author  = {mphilli and
               ValerioNeriGit and
               Tim Van Cann and
               Mitchellpkt},
  title     = {Converts English text to IPA notation},
  year      = {2019},
  url       = {https://github.com/mphilli/English-to-IPA/tree/a17c83eadddfd5888a1078b5632860cf474a5c2d},
}
```

**NetworkX**
```
Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, “Exploring network structure, dynamics, and function using NetworkX”, in Proceedings of the 7th Python in Science Conference (SciPy2008), Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008
```


## Getting Started

In order to run the project, we used **Python 3.9** on a linux based machine. After installing Python 3.9 the user must install the following pip-libaries to set up their environment 




```bash
  OpenNMT-py==2.2.0
  jellyfish==0.9.0
  eng-to-ipa==0.0.2
  pandas
  textdistance
  networkx
  openpyxl
  jellyfish
  xlsxwriter
  matplotlib

```

You will also need to install spacy, and download the "en_core_web_sm" file. More details can be found from spacy's [website](https://spacy.io/usage). We also recommend installing OpenNMT-py=2.2.0 first. 


## File Structure

The following files are used to generate the adjlists: 
```
main.py
parse.py
words.py
graph.py
```

The following files are used to generate the summary tables and calculates the network measures for the adjlists. 
```
analyze.py
```

### Main.py
main.py takes four arguments when it is run:

- -sf 
- -lw
- -size

The **sf** argument is asking if you have the "SUBTLEX-US-Copy" file in the directory. This file contains the word itself, the number of times it appears in the SUBTLEX-US database, and the phonetic transcription (IPA) of the word. 

If the file is missing then, the user can generate the file using the argument:
```
-sf False
```

The **lw** argument determines whether you want to use the lemmas only, or all of the words in the SUBTLEX-US database. 

If the user wants to use lemmas, then the user can use the following argument: 
```
-lw lemma
```

The **size** argument determines the number of words that the adjlist will contain.

If the user wants to have 1024 words in the adjlist. The user can use the following argument 
```
-size 1024
```

More information on the commands can he found by running the following command in the commandline: 
```
python3.9 main.py -h
``` 

**Example Command** 
If we have the phonetic transcriptions, and we want to use wordforms, and have 3000 words. 
```
python3.9 main.py -sf true -lw wordforms -size 3000
```

### Parse.py
#### create_file 
The create_file function generates a copy of the SUBTLEX-US file. 

### update_file
This updates the file created by create_file to store the phonetic transcription information in new columns. 

### Words.py
#### update_list 
The update_list function is used to trim our word count down by half based on the frequency of the word, until we can no longer trim our words by half. Afterwards words are randomly removed until we meet our desired size. 

#### add_words_to_list_from_file
This function takes the word, phonetic transcription in string and list form and uses the Word Class to create a "Word" object before assigning it to our list. 

#### add_words_to_list
This function does the same as above, but the file being used does not have the phonetic transcription. Therefore, it first uses eng-to-ipa to generate an phonetic transcription, if no transcription is found, then it uses the model created by  [@LonelyRider-cs](https://github.com/LonelyRider-cs). We afterwards read the output, and adjust the output to match the output of eng-to-ipa. 

#### update_ipa 
This function updates our phonetic transcriptions for the transcriptions that consist of two characters, but should be treated as one character with a length of 2.

#### words_without_pos 
This function would check how many words do not have a POS tag \
**Not Used** 

#### total_POS / total_pos_reading_from_file
This function would check how many words have a POS tag, and find the average number of POS for each word\
**Not Used**

#### frequency_distribution
Find the frequency of each POS tag, and then find the average POS for each word\
**Not Used**

### Graphs.py 
#### number_of_lemmas
This function takes our SUBTLEX-US dataset and returns the a list of lemmas

#### create_adjanceylist / create_adjanceylist_lemma
This function generates our adjancey list for our words/lemmas and an adjancey list for the phonetic transcription. 

#### create_graph 
This function generates the network in a png format / 
**Not used**  

### Analyze.py

To generate the summary tables for the wordform adjlistss, add the files name onto line 752 of analyze.py, inside of the list.

To generate the summary tables for the lemma adjlists, add the files names onto line 754 of analyze.py.

**Note:** The adjlists must be in the same folder as the analyze.py function 


#### validateWordEdgeList
This function validates our adjlists, and removes any self loops, and make sures words with the same root word are not connected to each other. This function also adds in the word "null" to the graph, as it was not added by the graphs.py file. This function also returns a validated adjlist file, which should be used for all calculations.

#### getSystemFactsWordForms / getSystemFactsLemmas
Calls the validateWordEdgeList function, and returns the following: 
- number of nodes
- number of island nodes
- number of hermit nodes
- number of nodes in the giant component 
- number of islands
- number of links/edges
- avg shortest path in the giant component 
- avg clustering coefficient in the giant component 
- degree assortativity
- max degree
- heterogeneity parameter K 


## Extensions

This project can be extended to use other corpora, including using different English corpora. First, prepare the data by putting the corpus data in an Excel file with orthographic words in a ‘Word’ column. The create_file() function must then be modified to create a copy of this file and use this new copied version. Next, we need to generate IPA translations using our existing add_words_to_list function. This function may need to be modified if there is no frequency count available by either providing a default value (easiest method) or changing the code to remove the FREQCount variable (not recommended as trimming our list uses median frequency). Once this has been completed, the functions can run as is (based on the original parameters in the readme), and then one can use the analyze.py function to process a new adjlist and return details about a network based on this adjust.

To extend the project to languages other than English, it is necessary to update how we get the phonetic transcriptions since our eng-to-ipa library and neural network model specifically converts English Text to IPA. To handle more languages, one either needs to find a suitable library or create a model to handle the new language. Once this has been accomplished, it will be necessary to update our functions to use this new library and/or model in our add_words_to_list()/add_words_to_list_from_file() commands. If there are any specific phonetic rules relevant to string edit distance (such as in English when two phonetic characters are combined and treated as one character), it is necessary to update our update_ipa() command with this information. Finally, follow the data preparation steps above to update our existing code to receive a new corpus.

While string edit distance is our metric for characterizing phonological similarity, there are other distance metrics one might want to use, such as PLD20 (Suárez et al. 2011, DOI: 10.3758/s13423-011-0078-9). To expand upon string edit distance, the conditional statement in the Levenshein distance code could be either changed or more conditions can be added. For PLD20, for example, we can get the average (for connected nodes) by calculating the average of the 20th closest neighbors using a for loop (we can also get neighbors of neighbors if needed). For nodes without neighbours, we can use a for loop to get the number of changes required for all of the words in our corpus, and then either sort it from least to most transitions, or get the average from a random set, average of the N most substitutions, or average of the N least substituion