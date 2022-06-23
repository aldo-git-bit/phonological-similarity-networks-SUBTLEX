from parse import *
from words import *
import eng_to_ipa as ipa
import subprocess
import jellyfish

def main():
    similar = 0
    sed_ignoring_zerocase = 0
    sed = 0
    no_ipa = 0

    words_pos_separated = []
    words_different = []
    # print("1")
    # create_file()
    # print("2")
    add_words_to_list(words_pos_separated)
    # # nan = words_without_pos(words_pos_separated)
    # # freq = total_pos(words_pos_separated, nan)
    # # print(freq)
    # # total_pos_reading_from_file()
    # # frequency_distribution(freq)
    # print("3")
    f = open("random_sample_3.txt", "w+")
    s = "word"
    t = "ipa"
    u = "ipa_model"
    f.write(f"{s:<30} \t {t:<30} \t {u:<30} \n")
    for i in range(0, len(words_pos_separated)):
        f.write(f'{words_pos_separated[i].WORD:<30} \t {words_pos_separated[i].IPA:<30} \t {words_pos_separated[i].IPA_model:<30}')
        f.write("\n")
    
    f.write("\n \n ")
    for i in range(0, len(words_pos_separated)):
        if words_pos_separated[i].IPA[len(words_pos_separated[i].IPA) - 1] == "*":
            no_ipa += 1
        else:
            if jellyfish.damerau_levenshtein_distance(words_pos_separated[i].IPA, words_pos_separated[i].IPA_model) == 0:
                similar += 1
                sed += jellyfish.damerau_levenshtein_distance(words_pos_separated[i].IPA, words_pos_separated[i].IPA_model)

            else:
                words_different.append(words_pos_separated[i])
                sed += jellyfish.damerau_levenshtein_distance(words_pos_separated[i].IPA, words_pos_separated[i].IPA_model)
                sed_ignoring_zerocase += jellyfish.damerau_levenshtein_distance(words_pos_separated[i].IPA, words_pos_separated[i].IPA_model)
                
    

    f.write(f"No IPA translation using library: {no_ipa} ({no_ipa / len(words_pos_separated) * 100}%) \n")
    f.write(f"IPA translation that is the same using the library and model: {similar} ({similar / (len(words_pos_separated) - no_ipa) * 100}%) \n")
    f.write(f"SED Average Including when SED is 0: {sed}/{len(words_pos_separated) - no_ipa} ({sed / (len(words_pos_separated) - no_ipa)}) \n")
    f.write(f"SED Average Excluding when SED is 0: {sed_ignoring_zerocase}/{len(words_different)} ({sed_ignoring_zerocase / len(words_different)}) \n")
    f.write(f"\n \n Words that have different IPA Transcriptions \n")

    for i in range(0, len(words_different)):
        f.write(f'{words_different[i].WORD:<30} \t {words_different[i].IPA:<30} \t {words_different[i].IPA_model:<30} \t String Edit Distance {jellyfish.damerau_levenshtein_distance(words_different[i].IPA, words_different[i].IPA_model):<3}')
        f.write("\n")

    # subprocess.run('bash ipa_translator.sh china', shell=True, capture_output=True, text=True)

if __name__ == "__main__":
    main()
