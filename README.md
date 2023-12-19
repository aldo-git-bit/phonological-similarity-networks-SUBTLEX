
## File Structure

The following files are used to generate the adjlists: 
```
main.py
parse.py
words.py
graph.py
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