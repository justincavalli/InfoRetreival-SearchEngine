from queue import PriorityQueue
from turtle import st

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import sys

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

def score_positions(docData1, docData2):
    positions1 = sorted([int(x) for x in docData1.split(':')[1].split(',')])
    positions2 = sorted([int(x) for x in docData2.split(':')[1].split(',')])

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
    return 1/answer
    
    

    

def score(documentName, documentData):
    score = 0

    parseByTerm = documentData.split(';')
    if(len(parseByTerm) == 1):
        # the score of a document with only one term is the count of the term
        score = int(documentData.split(':')[0])
    else:
        score = int(parseByTerm[0].split(':')[0])
        for i in range(1, len(parseByTerm)):
            score += int(parseByTerm[i].split(':')[0])
            score += score_positions(parseByTerm[i], parseByTerm[i-1])

    # add the document score tuple to the priorityQueue
    return (documentName, score)


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
        data = info[1]
        splitByDoc = data.split(';')
        for doc in splitByDoc:
            # take care of the few cases with empty string
            if(doc == ''):
                continue
            # parse out docname and info corresponding to it and place in the dict
            elif(doc[:10] in docTable.keys()):
                docTable[doc[:10]] += ';' + doc[10:]
            else:
                docTable[doc[:10]] = doc[10:]
    for doc in docTable.keys():
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

def main():
    query = input("Q> ")
    processedQuery = process(query)
    priorityQueue = termAtATimeRetrieval(processedQuery, 10)
    
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