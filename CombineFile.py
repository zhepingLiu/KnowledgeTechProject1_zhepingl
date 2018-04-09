misspell = open("2018S1-90049P1-data/misspell.txt", "r")
misspell_words = misspell.readlines()
correct = open("2018S1-90049P1-data/correct.txt", "r")
correct_words = correct.readlines()

for i in range(len(misspell_words)):
    print("Misspell %s Correct %s" % (misspell_words[i], correct_words[i]))