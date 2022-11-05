from queue import PriorityQueue
from turtle import st

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from math import sqrt
import string
import sys
import os

idf = {}
qtWeight = {}

def getInvertedList(term):
    # find the invertedIndex file based on the first letter of the word
    firstLetter = term[0]
    if 'a' <= firstLetter <= 'd':
        file = open('inv-index/AD_words.txt')
    elif 'e' <= firstLetter <= 'h':
        file = open('inv-index/EH_words.txt')
    elif 'i' <= firstLetter <= 'l':
        file = open('inv-index/IL_words.txt')
    elif 'm' <= firstLetter <= 'p':
        file = open('inv-index/MP_words.txt')
    elif 'q' <= firstLetter <= 't':
        file = open('inv-index/QT_words.txt')
    elif 'u' <= firstLetter <= 'z':
        file =open('inv-index/UZ_words.txt')
    
    line = file.readline()
    # read line by line to find the word
    while(line):
        if term == line.split()[0]:
            # return the entire line for the word
            return line
        line = file.readline()
    
    # if the word isn't found return false
    return False

def cosine(weights):
    # calculates cosine function based on document and query tf-idf weights
    numerator = 0
    docDenom = 0
    qDenom = 0
    for term in weights.keys():
        numerator += weights[term] * qtWeight[term]
        docDenom += weights[term] ** 2
        qDenom += qtWeight[term] ** 2
    
    return numerator / (sqrt(docDenom + qDenom))

def shortest(positions1, positions2):
    positions1 = sorted([int(x) for x in positions1])
    positions2 = sorted([int(x) for x in positions2])

     # find minimum difference psuedocode: https://www.tutorialspoint.com/program-to-find-minimum-difference-between-two-elements-from-two-lists-in-python#:~:text=Practical%20Data%20Science%20using%20Python&text=Suppose%20we%20have%20two%20lists,is%2010%20%2D%207%20%3D%203.&text=otherwise%2C,j%20%3A%3D%20j%20%2B%201
    answer = sys.maxsize
    i = 0
    j = 0

    while i < len(positions1) and j < len(positions2):
        answer = min(answer, abs(positions1[i] - positions2[j]))
        if positions1[i] < positions2[j]:
            i += 1
        else:
            j += 1
    return answer

def score_positions(docData):
    # calculate score_positions for given document
    score = 0
    # loop through the positions of two terms at a time
    for i in range(1, len(docData)):
        score += 1 / shortest(docData[i].split(':')[2].split(','), docData[i-1].split(':')[2].split(','))
    return score

def score(doc, docData):
    tf = {}
    weight = {}
    byTerm = docData.split(';')
    totalCount = 0
    for termInfo in byTerm:
        totalCount += int(termInfo.split(':')[1])

    # create dictionary of term frequencies (tf)
    for termInfo in byTerm:
        tf[termInfo.split(':')[0]] = int(termInfo.split(':')[1]) / totalCount

    for term in tf.keys():
        if(tf[term]):
            weight[term] = tf[term] * idf[term]     # tf-idf doc weighting
        else:
            weight[term] = 0    # weight is 0 if not in the doc
    # add the cosine and score_positions for the total document score
    return (doc, cosine(weight) + score_positions(byTerm))

def termAtATimeRetrieval(query, maxSize):
    docTable = {}
    invertedLists = []
    priorityQueue = []

    for term in query:
        # add all inverted lists for the words into invertedLists
        invertedList = getInvertedList(term)
        # if the term matches, add the invertedList
        if invertedList:
            invertedLists.append(invertedList)
    
    for currlist in invertedLists:
        # parsing out data for each doc
        info = currlist.split()
        term = info[0]
        data = info[1]
        splitByDoc = data.split(';')
        for doc in splitByDoc:
            # take care of the few cases with empty string
            if(doc == ''):
                continue
            # parse out docname and info corresponding to it and place in the dict
            elif(doc[:10] in docTable.keys()):
                docTable[doc[:10]] += ';' + term + ":" + doc[10:]
            else:
                docTable[doc[:10]] = term + ":" + doc[10:]

    for doc in docTable.keys():
        # score(doc, docTable[doc])
        priorityQueue.append(score(doc, docTable[doc]))
        priorityQueue.sort(reverse=True, key=lambda a: a[1])
        # after sorting, only keep the first 10 elements
        templist = []
        if len(priorityQueue) >= maxSize:
            for i in range(maxSize):
                templist.append(priorityQueue[i])
            priorityQueue = templist
    return priorityQueue

def process(query):
    # process the query the same way the txt docs were transformed
    output = []
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    # tokenize the words out
    line = query.translate(str.maketrans('', '', string.punctuation)).lower()
    tokenizeline = word_tokenize(line)
    for word in tokenizeline:
        # stem the words
        stemmedWord = ps.stem(word)
        # ignore stop words
        if stemmedWord not in stop_words and getInvertedList(stemmedWord):
            output.append(stemmedWord)

    # return the query as a list of words
    return output


def computeIDF(query):
    global idf
    # compute idf for each term in the query
    N = len(os.listdir('input-transform/'))         # total num of docs in the collection
    for term in query:
        nk = len(getInvertedList(term).split(';'))  # num of docs containing the term
        idf[term] = N/nk

def computeQTW(query):
    global qtWeight
    # calculate the query term weights and update the global variable for it
    for term in query:
        qtWeight[term] = (query.count(term) / len(query)) * idf[term]

def main():
    rawQuery = input('Q> ')
    query = process(rawQuery)
    computeIDF(query)
    computeQTW(query)
    priorityQueue = termAtATimeRetrieval(query, 10)

    if(len(priorityQueue) == 0):
        print('No results')
    else:
        # output the top 10 results
        print('Top 10 results:')
        i = 0
        while i < 10 and i < len(priorityQueue):
            file, score = priorityQueue[i]
            print(str(i+1) + '. aleph.gutenberg.org/' + file[0] + '/' + file[1] + '/' + file[2] + '/' + file[3] + '/' + file[0:5])
            i+=1

main()