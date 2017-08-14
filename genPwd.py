import csv
import itertools
import argparse
from threading import Thread

def loadPersonalsDatas(dictionary, dateList, wordList): #dateList must be empty
    for entry in dictionary:
        if entry[0].count('/') > 0:
            dateList.append(entry[0])
        else:
            wordList.append(entry[0])

def threadLauncher(wordList,dictionary):
    myWords = []
    temp = []
    for wordInList in wordList:
        myWords.append(word(wordInList))
    for i in myWords:
        temp.append(genObjects(i, dictionary))
    for thread in temp:
        thread.start()
    for thread in temp:
        thread.join()

    return myWords


#Generate all possible strings from 1 char to 4 char (BF)
def miniBf(string, list):
    res = ""
    dico = "abcdefghijklmnopqrstuvwxyz0123456789@&!:;,?./\\$*ù+-=%µ£€"
    if len(string)<4:
        for char in dico:
            res = string + char
            list.append(res)
            miniBf(res, list)

#Load CSV (LeetTab / Date Conversion / Personals infos)
def loadCsv(file, myDelimiter):
    res = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=myDelimiter)
        for i in reader:
            res.append(i)
    return res

#Take the leet table and juste get the lines usefull
def getSmallDic(word, dictionary):
    res = []
    word = list(set(word.lower()))
    for i in word:
        for j in dictionary:
            if i == j[0]:
                res.append(j)
    return res

#Class to generate Leet from a word
class word:
    #Initialisation
    def __init__(self, word):
        self.word = word
        self.done = []

    #Function to generate all leet possible
    def genWords(self, dictionary, string, pos):
        res = ""
        if len(string)<len(self.word):
            for j in self.word[pos:]:
                for i in dictionary:
                    if j.lower() == i[0]:
                        for k in i:
                            res = string + k
                            self.genWords(dictionary,res,pos+1)
                break

        else:
            self.done.append(string)

#Class to generate all dates format
class date:
    #Initialisation
    def __init__(self, date):
        if len(date.split('/')) == 3:
            self.day = date.split('/')[0]
            self.month = date.split('/')[1]
            self.year = [date.split('/')[2], date.split('/')[2][2:]]
        else:
            self.day = date.split('/')[0]
            self.month = date.split('/')[1]
            self.year = 0
        self.done = []

    #Generate all differents formats for a given date : d-m-y (little endian)/ m-d-y (middle endian)/ y-m-d (big endian)
    def genDatesFormat(self, dictionary):
        self.month = self.month.split(' ') #Transform string in list of strings
        for month in dictionary:
            if self.month[0] in month:
                self.month = month
                break
        if self.year != 0:
            temp = [self.day.split(' '), self.month, self.year]
            temp2 = [self.month, self.day.split(' '), self.year]
            temp3 = [self.year, self.month, self.day.split(' ')]
            temp = list(itertools.product(*temp))
            temp2 = list(itertools.product(*temp2))
            temp3 = list(itertools.product(*temp3))
            for x in temp2:
                temp.append(x)
            for x in temp3:
                temp.append(x)
        else:
            temp = [self.day.split(' '), self.month]
            temp2 = [self.month, self.day.split(' ')]
            temp = list(itertools.product(*temp))
            temp2 = list(itertools.product(*temp2))
            for x in temp2:
                temp.append(x)
        self.done = temp

#Function to combines all our results from leet words and dates : TO DO
def packing(list, file):


    if checkInFile(res) != 0:
        packing(list, file)
    else:
        writeInFile(res)

#Thread to generate leet for all words in personal infos
class genObjects(Thread):
    def __init__(self, word, dictionary):
        Thread.__init__(self)
        self.word = word
        self.dictionary = dictionary
        super(genObjects, self).__init__()

    def run(self):
        self.word.genWords(self.dictionary, "", 0)

#???? Is it usefull ????
def checkInFile(string, file):
    if string in file:
        return 0
    else:
        return 1

#MAIN
if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="file wich contains personals datas")
    args = vars(ap.parse_args())


    dico = loadCsv("leetTab.csv",";")
    dicoMonth = loadCsv("date.csv",";")
    dateList = []
    wordList = []
    loadPersonalsDatas(loadCsv(args["file"], ";"), dateList, wordList)
    myWords = threadLauncher(wordList, dico)
    for i in myWords:
        print(i.done)
    myDates = []
    #test = word("Alliacom")
    #garbage = []
    #miniBf("",garbage   )
    #smallDic = getSmallDic(test.word, dico)
    #test.genWords(smallDic, "" , 0)
    #print(test.done)
    #testD = date("22/01")
    #testD.genDatesFormat(dicoMonth)
    #print(testD.done)



    print("hi !")
