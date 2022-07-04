import networkx as nx
import matplotlib.pyplot as plt
import textdistance



def create_adjanceylist(words):
    f = open("words.adjlist", "w+")
    g = open("IPA.adjlist", "w+")
    h = open("List-output.txt", "w+")

    
    for i in range(0, len(words)):
        temp_array_word1 = []
        word_1 = words[i].IPA_LIST
        f.write(f"{words[i].WORD} ")
        g.write(f"{words[i].IPA} ")

        for k in range(0, len(word_1)):
            temp_array_word1.append(word_1[k])

            if word_1[k-1] + word_1[k] == "oʊ":
                temp_array_word1.pop()
                temp_array_word1.pop()
                temp_array_word1.append(word_1[k-1] + word_1[k])
            
        h.write(f"{temp_array_word1}")
        for j in range(0, len(words)):
            if i != j:
                temp_array_word2 = []
                word_2 = words[j].IPA_LIST
                for k in range(0, len(word_2)):
                    temp_array_word2.append(word_2[k])

                    if word_2[k-1] + word_2[k] == "oʊ":
                        temp_array_word2.pop()
                        temp_array_word2.pop()
                        temp_array_word2.append(word_2[k-1] + word_2[k])

                # print(f"{temp_array_word1} ...... {temp_array_word2}")
                if textdistance.levenshtein.distance(temp_array_word1, temp_array_word2) == 1:
                    f.write(f"{words[j].WORD} ")
                    g.write(f"{words[j].IPA} ")
                    
        f.write("\n")
        g.write("\n")
        h.write("\n")

    f.close()
    g.close()
    h.close()

def create_graph():
    graph = nx.read_adjlist('words.adjlist')
    nx.draw(graph,
            with_labels=True,
            node_color='black',
            node_size=18,
            font_size=8,
            verticalalignment='baseline',
            edge_color='grey')
    plt.savefig('graphhhhhhhhhh.png')
    plt.show()


