import csv
from threading import Thread

def loadCsv(file):
    res = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for i in reader:
            res.append(i)

    return res


def getSmallDic(word, dictionary):
    res = []
    word = list(set(word.lower()))
    for i in word:
        for j in dictionary:
            if i == j[0]:
                res.append(j)
    return res

class word:
    def __init__(self, word):
        self.word = word
        self.done = []

    def genWords(self, dictionary, string, pos):
        res = ""
        if len(string)<len(self.word):
            for j in self.word[pos:]:
                for i in dictionary:
                    if j in i:
                        for k in i:
                            res = string + k
                            self.genWords(dictionary,res,pos+1)
                break

        else:
            self.done.append(string)


    def checkExist(string):
        if string in self.done:
            return 0
        else:
            return 1

def bfBegtoEnd(mot):


    return res

def packing(list, file):


    if checkInFile(res) != 0:
        packing(list, file)
    else:
        writeInFile(res)

class genObjects(Thread):
    def __init__(self,word):
        Thread.__init__(self)
        self.word = word
        super(genObjects, self).__init__()

    def run(self):
        self.word.genWords()





def checkInFile(string, file):
    if string in file:
        return 0
    else:
        return 1


if __name__=="__main__":
    dico = loadCsv("leetTab.csv")
    test = word("Alliacom")
    smallDic = getSmallDic(test.word, dico)
    test.genWords(smallDic, "" , 0)

    print("hi !")
