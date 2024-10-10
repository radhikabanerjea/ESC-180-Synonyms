# Maria Salonga & Radhika Banerjea
# Monday, December 5, 2022



'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2022.
'''

import math
import re

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):

    dot = 0
    for key in vec1.keys():
        try:
            dot = dot + vec1[key]*vec2[key]
        except:
            pass

    list1 = list(vec1.values())
    list2 = list(vec2.values())
    list1 = [int(x) for x in list1]
    list2 = [int(x) for x in list2]
   
    sumsqvec1 = 0
    sumsqvec2 = 0
    
    for v in range(len(list1)):
        sumsqvec1 = sumsqvec1 + (list1[v]**2)

    for x in range(len(list2)):
        sumsqvec2 = sumsqvec2 + (list2[x]**2)


    return dot/math.sqrt((sumsqvec1)*(sumsqvec2))


def build_semantic_descriptors(sentences):

    temp_word_list = []
    for index in range(0, len(sentences)):
        temp_word_list = temp_word_list + sentences[index]

    word_list = set(temp_word_list)

    actual_dict = {}

    for word in word_list:
        print("In big for loop")
        list_of_desired_sentences = []  # list of words from all sentenves that invlude the desired word
        value_dict = {} # plave holder for kay-value pair of the desired ie. {word : {and:3. i:2......}}

        # weeding out sentences that don't contain the desired word
        for index in range(0, len(sentences)):
            if word in sentences[index]:
                #creates giant list with words of all sentences conatining desired word
                list_of_desired_sentences = list_of_desired_sentences + sentences[index]


        no_duplicate_every_word = set(list_of_desired_sentences)
        for sentenceword in no_duplicate_every_word:
            if sentenceword != word:
                value_dict[sentenceword] = list_of_desired_sentences.count(sentenceword)

        actual_dict[word] = value_dict
    print("im about to return smthg")
    return actual_dict
    

def build_semantic_descriptors_from_files(filenames):

    print("in build semantic descriptors")

    sublist = []

    for x in filenames:
        print("in for loop")
        filetext = open(x, "r", encoding="latin1")
        string = filetext.read()
        string = string.replace(';', '')
        string = string.replace(':', '')
        string = string.replace(',', '')
        string = string.replace('-', '')
        string = string.replace('--', '')
        string = string.lower()
        sentenceList = list(filter(None, re.split('[.!?]', string))) 

        for sentence in sentenceList:
            tempSent = ""
            tempSent = sentence.split(" ")
            tempSent = [value for value in tempSent if value != '']
            sublist.append(tempSent)
    print("I got out of the for loops")
    return build_semantic_descriptors(sublist)
        
        
def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    tempSimilarity = 0
    highestSimilarity = None
    bestChoice = None

    for c in choices:
        try:
            tempSimilarity = similarity_fn(semantic_descriptors[c], semantic_descriptors[word])
        except:
            tempSimilarity = -1
        

        if highestSimilarity == None:
            highestSimilarity = tempSimilarity
            bestChoice = c
        else:
            if tempSimilarity > highestSimilarity:
                tempSimilarity = highestSimilarity
                bestChoice = c
   
    return bestChoice


def run_similarity_test(filename, semantic_descriptors, similarity_fn):

    print("Running similarity test")

    filetext = open(filename, "r", encoding="latin1")
    list = filetext.readlines()
    denominator = len(list)
    counter = 0
    for line in list:
        listcheck = line.split(" ")
        if listcheck[1] == most_similar_word(listcheck[0], listcheck[2:], semantic_descriptors, similarity_fn):
            counter = counter + 1
    
    return (counter/denominator)*100

        
if __name__ == '__main__':
    #print(cosine_similarity({"a": 7, "j": 9, "c": 5}, {"b": 1, "c": 3, "d": 8, "j":19,"l":1,"m":3,"b":5}))
    
    semantic_descriptors = build_semantic_descriptors_from_files(["text1.txt","text2.txt"])
    
    print(semantic_descriptors)

    res = run_similarity_test("testCases.txt", semantic_descriptors, cosine_similarity)

    print(res, " of the guesses were correct.")
