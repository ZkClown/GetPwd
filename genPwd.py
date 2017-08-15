import csv
import itertools
import argparse
from threading import Thread
import os

#----------------------------------Classes-------------------------------------------------#
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

#------------------------------------------------------------------------------------------#

#----------------------------------Threads-------------------------------------------------#
#Thread to generate leet for all words in personal infos
class genObjects(Thread):
    def __init__(self, word, dictionary):
        Thread.__init__(self)
        self.word = word
        self.dictionary = dictionary
        super(genObjects, self).__init__()

    def run(self):
        self.word.genWords(self.dictionary, "", 0)

#Thread to generate dates format for all dates
class genDates(Thread):
    def __init__(self, date, dictionary):
        Thread.__init__(self)
        self.word = date
        self.dictionary = dictionary
        super(genDates, self).__init__()

    def run(self):
        self.word.genDatesFormat(self.dictionary)

class partCombine(Thread):
    def __init__(self,list, begValue, end, index):
        Thread.__init__(self)
        self.begValue = begValue
        self.end = end
        self.index = index
        self.list = list
        super(partCombine, self).__init__()

    def run(self):
        packing2(self.list, self.begValue, self.end, self.index)


#------------------------------------------------------------------------------------------#
#----------------------------------Thread Launchers----------------------------------------#
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

def threadDateLauncher(dateList,dictionary):
    myDates = []
    temp = []
    for dateInList in dateList:
        myDates.append(date(dateInList))
    for i in myDates:
        temp.append(genDates(i, dictionary))
    for thread in temp:
        thread.start()
    for thread in temp:
        thread.join()

    return myDates

def threadCombiner(list, index):
    file = open("init.txt","w")
    for word in list:
        file.write(word+"\n")
    lastValue = 0
    threadNumber = 0
    step = 100
    tmp = []
    for i in range(0,len(list)):
        if(i%step == 0):
            tmp.append(partCombine(list, lastValue, i, threadNumber))
            lastValue = i
            threadNumber += 1
    if(lastValue!=len(list)):
        tmp.append(partCombine(list, lastValue, len(list), threadNumber))
    for thread in tmp:
        thread.start()
    print("Fin lancement thread")
    for thread in tmp:
        thread.join()
    os.system("cat *.txt > output"+str(index)+" && rm *.txt")




#------------------------------------------------------------------------------------------#
#----------------------------------Functions-----------------------------------------------#
def loadDatesWithSeparators(myDates):
    res = []
    separators = " -_/|"
    for date in myDates:
        for dateFormated in date.done:
            if len(dateFormated) == 2:
                for sep in separators:
                    res.append(dateFormated[0]+sep+dateFormated[1])
                res.append(dateFormated[0]+dateFormated[1])
            else:
                for sep in separators:
                    res.append(dateFormated[0]+sep+dateFormated[1]+sep+dateFormated[2])
                res.append(dateFormated[0]+dateFormated[1]+dateFormated[2])
    return res

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

def threadDateLauncher(dateList,dictionary):
    myDates = []
    temp = []
    for dateInList in dateList:
        myDates.append(date(dateInList))
    for i in myDates:
        temp.append(genDates(i, dictionary))
    for thread in temp:
        thread.start()
    for thread in temp:
        thread.join()

    return myDates

#Generate all possible strings from 1 char to 4 char (BF)
def miniBf(string, list):
    res = ""
    dico = "abcdefghijklmnopqrstuvwxyz0123456789@&!:;,?./\\$*ù+-_=%µ£€()[]|~#\{\}@^"
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


#Function to combines all our results from leet words and dates : technically it works ... but use too much rssources
def packing(myWords, myDates, garbage):
    res = []
    dates = loadDatesWithSeparators(myDates)
    words = []
    for word in myWords:
        for done in word.done:
            words.append(done)
    #print(len(words))
    temp = ["words","dates","garbage"]
    iter2 = list(itertools.product(temp, repeat=2))
    iter3 = list(itertools.product(temp, repeat=3))
    iter4 = list(itertools.product(temp, repeat=4))
    for i in iter2:
        res.append(list(itertools.product(eval(i[0]),eval(i[1]))))
    #    break
    for i in iter3:
        res.append(list(itertools.product(eval(i[0]),eval(i[1]),eval(i[2]))))
    for i in iter3:
        res.append(list(itertools.product(eval(i[0]),eval(i[1]),eval(i[2]),eval(i[3]))))
    return res

#list of lists to simple list
def lolToSl(myWords):
    words = []
    for word in myWords:
        for done in word.done:
            words.append(done)
    return words

def packing2(list, start, end, index):
    file = open(str(index)+".txt","w")
    for i in range(start,end):
        for j in range(0,len(list)):
            file.write(list[i]+list[j]+"\n")

    file.close()

#------------------------------------------------------------------------------------------#

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
    myDates = threadDateLauncher(dateList, dicoMonth)
    garbage = ["1","2"]

    threadCombiner(lolToSl(myWords),0)
    #packing(myWords, myDates, garbage)
    #miniBf("",garbage)


    #test = word("Alliacom")
    #
    #smallDic = getSmallDic(test.word, dico)
    #test.genWords(smallDic, "" , 0)
    #print(test.done)
    #testD = date("22/01")
    #testD.genDatesFormat(dicoMonth)
    #print(testD.done)



    print("hi !")
