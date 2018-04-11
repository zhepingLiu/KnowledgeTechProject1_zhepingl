'''
    Knowledge Technology Project 1
    Zheping Liu, 683781, zhepingl
'''
import time
import editdistance
import re
from collections import Counter
#Read misspelled words from .txt files, Apply two different algorithms to 
#correct them, and comparing the results to all entries in the correct 
#.txt file

#Algorithm 1: Global Edit Distance
#Algorithm 2: N-gram Distance
#Algorithm 3: Neighbourhood Search

#Scope of Global Edit Distance and N-gram distance
SCOPE = 2
#N in the N-gram
NGRAM = 2

MATCH = 0
HASH = "#"

# open and read the three resource files into arrays
misspell = open("2018S1-90049P1-data/misspell.txt", "r")
misspell_words = misspell.readlines()
correct = open("2018S1-90049P1-data/correct.txt", "r")
correct_words = correct.readlines()
dictionary = open("2018S1-90049P1-data/dictionary.txt", "r")
dictionary_words = dictionary.readlines()

# the dictionary records every corrected word
corrections = dict()
# the dictionary records every failed word
failure = dict()
#Algorithm 1: Global Edit Distance
'''
    Spell Correction algorithm using Global Edit Distance
'''
def global_edit_distance():
    start_time = time.time()
    attempt = 0
    print("Global Edit Distance Result with Scope = %d" % SCOPE)
    #find all potential attempts within defined scope for each misspelled word
    for i in range(len(misspell_words)):
        potential_words = []
        #record all words failed to match the correct one
        failure_words = []
        for j in range(len(dictionary_words)):
            if editdistance.eval(misspell_words[i], 
                                dictionary_words[j]) <= SCOPE:
                potential_words.append(dictionary_words[j])
                attempt += 1
        
        #compare all potential attempts with the correct word
        for k in range(len(potential_words)):
            if editdistance.eval(potential_words[k], correct_words[i]) == MATCH:
                corrections[misspell_words[i]] = potential_words[k]
            else:
                failure_words.append(potential_words[k])
                failure[misspell_words[i]] = failure_words
    
    print_correction(corrections, failure, attempt, start_time)


#Algorithm 2: N-gram Distance
'''
    Spell Correction algorithm using N-gram
'''
def ngram_search():
    start_time = time.time()
    attempt = 0
    ngram_dict = []
    print("N-gram Distance Result with n = %d, scope = %d" % (NGRAM, SCOPE))

    #split words in dictionary into n-grams
    for j in range(len(dictionary_words)):
            ngram_dict.append(ngram_split(NGRAM, dictionary_words[j]))

    #find all potential attempts within defined scope for each misspelled word
    for i in range(len(misspell_words)):
        potential_words = []
        failure_words = []
        #split misspelled words into n-grams
        nList_misspell = ngram_split(NGRAM, misspell_words[i])

        #compute n-gram distance between misspelled word 
        #and each dictionary word
        for j in range(len(dictionary_words)):
            nList_dict = ngram_dict[j]
            result = ngram_compare(nList_misspell, nList_dict)

            if result <= SCOPE:
                potential_words.append(dictionary_words[j])
                attempt += 1
        #compare all potential attempts with the correct word
        for k in range(len(potential_words)):
            if potential_words[k] == correct_words[i]:
                corrections[misspell_words[i]] = potential_words[k]
            else:
                failure_words.append(potential_words[k])
                failure[misspell_words[i]] = failure_words

    print_correction(corrections, failure, attempt, start_time)

'''
    Split text into n-gram segments n is the length of each segment
'''
def ngram_split(n, text):
    nList = []
    #add '#' at both the begining and the end
    if n > 1:
        text = HASH + text + HASH

    for i in range(len(text) - (n-1)):
        nList.append(text[i:i+n])

    return nList

'''
    Compare and compute the score for two n-gram lists
'''
def ngram_compare(list1, list2):
    common = 0

    for i in range(len(list1)):
        if list1[i] in list2:
            common += 1
    
    result = len(list1) + len(list2) - 2 * common
    return result

#Algorithm 3: Neighbourhood Search
'''
    Spell correction algorithm using neighbourhood search without selecting
    the one with maximum probability
'''
def neighbourhood_search_candidates():
    start_time = time.time()
    attempt = 0
    print("Neighbourhood Search Result")
    
    for i in range(len(misspell_words)):
        #find all potential attempts within defined number of edits
        potential_words = candidates(misspell_words[i])
        failure_words = []
        attempt += len(potential_words)
        
        #compare each attempt with correct word
        for word in potential_words:
            if (word == correct_words[i].rstrip()):
                corrections[misspell_words[i]] = word
            else:
                failure_words.append(word)
                failure[misspell_words[i]] = failure_words
    print_correction(corrections, failure, attempt, start_time)

'''
    Print the result of correction and percentage corrected
'''
def print_correction(corrections, failure, attempt, start_time):
    recall = len(corrections) / len(correct_words)
    percision = len(corrections) / attempt

    print("###Total corrected number : %d" % len(corrections))

    # Print Recall
    print("###Recall : %f%%" % (recall * 100))
    # Print Percision
    print("###Percision : %f%%" % (percision * 100))
    # Print Runtime
    print("###Total time spent : %s seconds" % (time.time() - start_time))

    # Print corrected words
    print("###Words Corrected###")
    for key, value in corrections.items():
        print("Misspell : %s Correct : %s" % (key, value))
    
    # Print failed words
    print("\n###Words Failed###")
    for key, value in failure.items():
        for i in range(len(value)):
            print("Misspell : %s Failed : %s" % (key, value[i]))

'''
    Source : How to Write a Spelling Corrector
    Author : Peter Norvig
'''
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('2018S1-90049P1-data/dictionary.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) 
            or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def edits3(word):
    return (e3 for e1 in edits1(word) for e2 in edits1(e1) for e3 in edits1(e2))

'''
    Run different spelling correction algorithms
'''
global_edit_distance()
ngram_search()
neighbourhood_search_candidates()