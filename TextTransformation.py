# use python natural language toolkit to handle stemming, tokenizing, stopwords 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

from zipfile import ZipFile
import io
import os


def isdir(z, name):
    return any(x.startswith("%s/" % name.rstrip("/")) for x in z.namelist())

def transformText(filepath, filename):
    # setup a porter stemmer and english stop words
    zipname = filename
    print(filepath)

    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    # read text files in a zip: https://stackoverflow.com/questions/15282651/how-do-i-read-text-files-within-a-zip-file
    with ZipFile(filepath) as zf:

        # some txt files are burried with another directory. This resolves that case
        if isdir(zf, zipname + '/'):
            zipname += '/' + zipname
        #
        with io.TextIOWrapper(zf.open(zipname + ".txt"), encoding="ISO-8859-1") as f:

            # read one line at a time
            newFile = open("input-transform/" + filename + ".txt", "w")
            line = f.readline()
            while line:
                newline = ""

                # tokenize the line
                line = line.translate(str.maketrans('', '', string.punctuation)).lower()    # remove punctuations and make lowercase
                tokenizeline = word_tokenize(line)

                for word in tokenizeline:

                    # stem the words one by one in the line
                    stemmedWord = ps.stem(word)

                    # ignore the stop words
                    if stemmedWord not in stop_words:
                        newline += stemmedWord + " "

                # write the transformed line to the new file
                newFile.write(newline)
                line = f.readline()
            newFile.close()
            f.close()

# recursively traverse deeper into directory until finding a file
def findFile(directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            # zip file is found, now transform it
            transformText(directory + "/" + filename, filename[:len(filename)-4]) #strip off extension
        else:
            # directory is found, recursively search it
            findFile(directory + "/" + filename)

# search teh input-files directory for the zip files
directory = "input-files/aleph.gutenberg.org/1"#/0/0/0"
findFile(directory)



