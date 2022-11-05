import os
class DocData:
    def __init__(self, position_list = []):
        self._count = 1
        self._positions = position_list

    def get_count(self):
        return self._count

    def get_positions(self):
        return self._positions

    def add_position(self, position):
        self._positions.append(position)

    def increment_count(self):
        self._count += 1

    def __str__(self):
        return str(self._count) + ":" + ",".join(str(x) for x in self._positions)


def shard():
    
    directory = 'input-transform/'
    AD_words = open('inv-index/AD_words.txt', 'w')
    EH_words = open('inv-index/EH_words.txt', 'w')
    IL_words = open('inv-index/IL_words.txt', 'w')
    MP_words = open('inv-index/MP_words.txt', 'w')
    QT_words = open('inv-index/QT_words.txt', 'w')
    UZ_words = open('inv-index/UZ_words.txt', 'w')

    for filename in os.listdir(directory):
        print(filename)
        currPos = 0
        file = open(directory + filename, 'r')
        # files are technically 1 line, because no \n where written to it
        for word in file.readline().split():
            currPos += 1
            firstLetter = word[0]
            data = word + ":" + filename + ":" + str(currPos) + ' '
            if 'a' <= firstLetter <= 'd':
                AD_words.write(data)
            elif 'e' <= firstLetter <= 'h':
                EH_words.write(data)
            elif 'i' <= firstLetter <= 'l':
                IL_words.write(data)
            elif 'm' <= firstLetter <= 'p':
                MP_words.write(data)
            elif 'q' <= firstLetter <= 't':
                QT_words.write(data)
            elif 'u' <= firstLetter <= 'z':
                UZ_words.write(data)
        
        
        file.close()
    
    AD_words.close()
    EH_words.close()
    IL_words.close() 
    MP_words.close()
    QT_words.close()
    UZ_words.close()



def merge():
   
    directory = 'inv-index/'

    for filename in os.listdir(directory):
        print(filename)
        index = {}
        file = open(directory + filename, 'r')
        # files are technically 1 line, because no \n where written to it
        for element in file.readline().split():
            decode = element.split(':')
            word = decode[0]
            txtfile = decode[1]
            location = decode[2]

            if not word in index:
                index[word] = {}
                index[word][txtfile] = DocData([location])
            elif not txtfile in index[word]:
                index[word][txtfile] = DocData([location])
            else:
                index[word][txtfile].increment_count()
                index[word][txtfile].add_position(location)
        file.close()

        # overwrite the file with word data aggregated/merged
        newFile = open(directory + filename, 'w')
        for key in sorted(index.keys()):
            output = str(key) + " "
            for doc in index[key]:
                output += str(doc) + ":" + str(index[key][doc]) + ";"
            newFile.write(output + "\n")
        newFile.close()



def main():
    shard()
    merge()

main()
