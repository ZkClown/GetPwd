import csv
from threading import Thread

def loadCsv(file):
    res = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for i in reader:
            res.append(i)

    return res

class word:
    def __init__(self, word):
        self.word = word
        self.done = []

    def genWords(dictionary):
        res = ""







        if self.checkExist(res) != 0:
            self.genWords()
        else:
            self.done.append(res)


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
    print("hi !")
