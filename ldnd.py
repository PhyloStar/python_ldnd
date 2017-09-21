import distances
import sys
from collections import defaultdict
import itertools as it

char_list = []

def read_data_ielex_type(fname):
    line_id = 0
    data_dict = defaultdict(lambda : defaultdict())
    cogid_dict = defaultdict(lambda : defaultdict())
    words_dict = defaultdict(lambda : defaultdict(list))
    langs_list = []
    concepts_list = []
    f = open(fname)
    header = f.readline().strip("\n").split("\t")
    word_idx = header.index("tokens")

    for line in f:
        line = line.strip()
        arr = line.split("\t")
        lang, iso, concept = arr[0], arr[1], arr[2]
        
        if len(arr) < 4:
            continue

        if " " in arr[word_idx]:
            asjp_word = arr[word_idx].split(" ")
        else:
            asjp_word = arr[word_idx]

        for ch in asjp_word:
            if ch not in char_list:
                char_list.append(ch)

        if len(asjp_word) < 1:
            continue
        
        data_dict[concept][line_id,lang] = asjp_word
        
        words_dict[lang][concept].append(asjp_word)
        
        if lang not in langs_list:
            langs_list.append(lang)
        if concept not in concepts_list:
            concepts_list.append(concept)
        line_id += 1
    f.close()
    print("Concepts List ", list(data_dict.keys()), sep="\n")
    print("Character List ", char_list, sep="\n")
    print("Languages List ", langs_list, len(langs_list),sep="\n")
    
    return (data_dict, words_dict, langs_list, concepts_list)

def get_word_dist(w1, w2):
    score = 0.0
    for x, y in it.product(w1, w2):
        score += distances.ldn(x, y)
    return score/(len(w1)*len(w2))
    
def get_lang_distance(words_dict, langs_list, product_concepts):
    langDistance = defaultdict(float)

    for l1, l2 in it.combinations(langs_list, r=2):
        num, n_num, denom, n_denom = 0.0, 0.0, 0.0, 0.0
        
        for c1, c2 in product_concepts:
            if c1 in words_dict[l1] and c2 in words_dict[l2]:
                w1 = words_dict[l1][c1]
                w2 = words_dict[l2][c2]
                if c1 == c2:
                    n_num += 1.0
                    num += get_word_dist(w1, w2)
                else:
                    n_denom += 1.0
                    denom += get_word_dist(w1, w2)
                    
        print(l1, l2, (num*n_denom)/(n_num*denom))

    return langDistance

data_dict, words_dict, langs_list, concepts_list = read_data_ielex_type(sys.argv[1])
product_concepts = [(x,y) for x, y in it.product(concepts_list, concepts_list)]
get_lang_distance(words_dict, langs_list, product_concepts)
