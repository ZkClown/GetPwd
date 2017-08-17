#!/usr/bin/python3
# -*- coding: utf-8 -*-

#----------------------------------Credits-------------------------------------------------#
#
#                          Made by Squadella & ZkClown                                     #
#
#------------------------------------------------------------------------------------------#
#----------------------------------Imports-------------------------------------------------#


import csv
import itertools
import argparse
from threading import Thread
import os
import datetime

#------------------------------------------------------------------------------------------#
#----------------------------------Classes-------------------------------------------------#
#Class to generate Leet from a word
class word:
    #Initialisation
    def __init__(self, word):
        self.word = word
        self.done = []
        self.done2 = []

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

            if(len(self.day) == 1):
                self.day = self.day.split(' ')
                self.day.append("0"+self.day[0])
            else:
                if int(self.day) < 9:
                    self.day = self.day.split(' ')
                    self.day.append(self.day[0][-1:])
                else:
                    self.day = self.day.split(' ')
            self.month = date.split('/')[1]
            self.year = [date.split('/')[2], date.split('/')[2][2:]]
        else:
            self.day = date.split('/')[0]
            if(len(self.day) == 1):
                self.day = self.day.split(' ')
                self.day.append("0"+self.day[0])
            else:
                if int(self.day) < 9:
                    self.day = self.day.split(' ')
                    self.day.append(self.day[0][-1:])
            self.month = date.split('/')[1]
            self.year = 0
        self.done = []
        self.done2 = []

    #Generate all differents formats for a given date : d-m-y (little endian)/ m-d-y (middle endian)/ y-m-d (big endian)
    def genDatesFormat(self, dictionary):
        self.month = self.month.split(' ') #Transform string in list of strings
        for month in dictionary:
            if self.month[0] in month:
                self.month = month
                break
        if self.year != 0:
            temp = [self.day, self.month, self.year]
            temp2 = [self.month, self.day, self.year]
            temp3 = [self.year, self.month, self.day]
            temp = list(itertools.product(*temp))
            temp2 = list(itertools.product(*temp2))
            temp3 = list(itertools.product(*temp3))
            for x in temp2:
                temp.append(x)
            for x in temp3:
                temp.append(x)
            temp4 = [self.day, self.month]
            temp5 = [self.month, self.day]
            temp4 = list(itertools.product(*temp4))
            temp5 = list(itertools.product(*temp5))
            for x in temp4:
                temp.append(x)
            for x in temp5:
                temp.append(x)
            temp.append([self.year[0]])
            temp.append([self.year[1]])

        else:
            temp = [self.day, self.month]
            temp2 = [self.month, self.day]
            temp = list(itertools.product(*temp))
            temp2 = list(itertools.product(*temp2))
            for x in temp2:
                temp.append(x)
        self.done = temp

    def convertDoneInList(self):
        now = datetime.datetime.now()
        res = [self]
        self.done2 = loadDatesWithSeparators(res)
        self.done2.remove(str(now.year))
        #print(self.done)

    def reasignDone(self,list):
        self.done = list

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
    def __init__(self,list, begValue, end, index, diff, myWords, myDates):
        Thread.__init__(self)
        self.begValue = begValue
        self.end = end
        self.index = index
        self.list = list
        self.diff = diff
        self.myWords = myWords
        self.myDates = myDates
        super(partCombine, self).__init__()

    def run(self):
        packing(self.list, self.begValue, self.end, self.index, self.diff, self.myWords, self.myDates)

class partCombNext(Thread):
    def __init__(self,list, begValue, end, index, diff, myWords, myDates):
        Thread.__init__(self)
        self.begValue = begValue
        self.end = end
        self.index = index
        self.list = list
        self.diff = diff
        self.myWords = myWords
        self.myDates = myDates
        super(partCombNext, self).__init__()

    def run(self):
        packNext(self.list, self.begValue, self.end, self.index, self.diff, self.myWords, self.myDates)

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

def threadCombiner(list, diff, myWords, myDates):
    initList(list)
    lastValue = 0
    threadNumber = 1
    step = int(len(list)/3)
    tmp = []
    for i in range(1,len(list)):
        if(i%step == 0):
            tmp.append(partCombine(list, lastValue, i, threadNumber, diff, myWords, myDates))
            lastValue = i
            threadNumber += 1
    if(lastValue!=len(list)):
        tmp.append(partCombine(list, lastValue, len(list), threadNumber, diff, myWords, myDates))
    for thread in tmp:
        thread.start()
    print("Fin lancement thread")
    for thread in tmp:
        thread.join()
    print("Packing")
    os.system("cat ./buffer/*.txt > ./buffer/output && rm ./buffer/*.txt")

def threadCombNext(list, rec, diff, myWords, myDates):

    for j in range(1,rec):
        lastValue = 0
        threadNumber = 0
        step = int(len(list)/3)
        tmp = []
        for i in range(1,len(list)):
            if(i%step == 0):
                tmp.append(partCombNext(list, lastValue, i, threadNumber, diff, myWords, myDates))
                lastValue = i
                threadNumber += 1
        if(lastValue!=len(list)):
            tmp.append(partCombNext(list, lastValue, len(list), threadNumber, diff, myWords, myDates))
        for thread in tmp:
            thread.start()
        print("Fin lancement thread")
        for thread in tmp:
            thread.join()
        print("Packing")
        os.system("cat ./buffer/*.txt > ./buffer/output"+str(j)+" && rm ./buffer/*.txt")


#------------------------------------------------------------------------------------------#
#----------------------------------Functions-----------------------------------------------#

#----------------------------------Loading Csv---------------------------------------------#
def loadDatesWithSeparators(myDates):
    res = []
    separators = "-_/|"
    now = datetime.datetime.now()
    for date in myDates:
        for dateFormated in date.done:
            if len(dateFormated) == 2:
                for sep in separators:
                    res.append(dateFormated[0]+sep+dateFormated[1])
                res.append(dateFormated[0]+dateFormated[1])
            elif len(dateFormated) == 3:
                for sep in separators:
                    res.append(dateFormated[0]+sep+dateFormated[1]+sep+dateFormated[2])
                res.append(dateFormated[0]+dateFormated[1]+dateFormated[2])
            else:
                res.append(dateFormated[0])
    res.append(str(now.year))
    return res

def loadPersonalsDatas(dictionary, dateList, wordList): #dateList must be empty
    for entry in dictionary:
        if entry[0].count('/') > 0:
            dateList.append(entry[0])
        else:
            wordList.append(entry[0])

#Load CSV (LeetTab / Date Conversion / Personals infos)
def loadCsv(file, myDelimiter):
    res = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=myDelimiter)
        for i in reader:
            res.append(i)
    return res



#----------------------------------Utils---------------------------------------------------#
#Take the leet table and juste get the lines usefull
def getSmallDic(word, dictionary):
    res = []
    word = list(set(word.lower()))
    for i in word:
        for j in dictionary:
            if i == j[0]:
                res.append(j)
    return res

#list of lists to simple list
def lolToSl(myWords):
    words = []
    for word in myWords:
        for done in word.done:
            words.append(done)
    return words

#Generate all possible strings from 1 char to 4 char (BF)
def miniBf(string, list):
    res = ""
    dico = "abcdefghijklmnopqrstuvwxyz0123456789@&!:;,?./\\$*ù+-_=%µ£€()[]|~#\{\}@^"
    if len(string)<4:
        for char in dico:
            res = string + char
            list.append(res)
            miniBf(res, list)


#------------------------------------------------------------------------------------------#

#----------------------------------Writing-------------------------------------------------#
def initList(list):
    file = open("./buffer/000","w")
    for word in list:
        file.write(word+"\n")
    file.close()

def packing(list, start, end, index, diff , myWords, myDates):
    for date in myDates:
        date.convertDoneInList()
        print(date.done2)
    for word in myWords:
        word.done2 = word.done
    flag = 0
    flag2 = 0
    j = 0
    temp = ""
    file = open("./buffer/"+str(index).zfill(3)+".txt","w")
    if diff != 1:
        for i in range(start,end):
            for j in range(0,len(list)):
                file.write(list[i]+list[j]+"\n")
    else:
        for i in range(start,end):
            while j < len(list):
                if flag2 == 0:
                    for word in myWords+myDates:
                        if list[i] in word.done2 and list[j] in word.done2:
                            j += len(word.done2)
                            break
                        elif list[j] in word.done2:
                            temp = word.done2[-1]
                            flag2 = 1
                            break
                    #print(i, j, len(list))
                    file.write(list[i]+list[j]+"\n")
                    j += 1
                else:
                    if list[j] == temp:
                        flag2 = 0
                    file.write(list[i]+list[j]+"\n")
                    j += 1
            temp = ""
            flag2 = 0
            j = 0
    file.close()

def packNext(list, startValue,endValue,index, diff, myWords, myDates):
    flag = 0
    file = open("./buffer/"+str(index).zfill(3)+".txt","w")
    for i in range(startValue, endValue):
        file2 = open("./buffer/output", "r")
        for line in file2:
            if diff != 1:
                file.write(list[i]+line)
            else:
                if len(list[i].split('/')) != 1:
                    for date in myDates:
                        if list[i] in date.done:
                            for x in date.done:
                                if x in line:
                                    flag = 1
                                    break
                            if flag == 1:
                                break
                    if flag == 0:
                        file.write(list[i]+line)
                    flag = 0
                elif len(list[i].split('/')) == 1:
                    for word in myWords:
                        if list[i] in word.done:
                            for x in word.done:
                                if x in line:
                                    flag = 1
                                    break
                            if flag == 1:
                                break
                    if flag == 0:
                        file.write(list[i]+line)
                    flag = 0
        file2.close()

    file.close()



#------------------------------------------------------------------------------------------#

#----------------------------------Main----------------------------------------------------#
if __name__=="__main__":

    wordList = []
    dateList = []
    garbage = []

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="file wich contains personals datas")
    ap.add_argument("-r", "--recurence", help="Number of iterations")
    ap.add_argument("-b", "--brute", help="Activate brute force, 1 to active")
    ap.add_argument("-d", "--difference", help="Activate the re usage of a same info more than once, 1 to activate")
    arg = ap.parse_args()
    args = vars(ap.parse_args())

    dico = loadCsv("leetTab.csv",";")
    dicoMonth = loadCsv("date.csv",";")
    loadPersonalsDatas(loadCsv(args["file"], ";"), dateList, wordList)

    myWords = threadLauncher(wordList, dico)
    myDates = threadDateLauncher(dateList, dicoMonth)

    if arg.brute:
        if args["brute"] == "1":
            miniBf("", garbage)

    if arg.recurence:
        if args["recurence"] in "0123456789":
            if int(args["recurence"]) > 0:
                if args["difference"] == "1":
                    threadCombiner(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage, 1, myWords, myDates)
                else:
                    threadCombiner(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage, 0, [], [])
                if int(args["recurence"]) > 1:
                    if args["difference"] == "1":
                        threadCombNext(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage,int(args['recurence']), 1, myWords, myDates)
                    else:
                        threadCombNext(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage,int(args['recurence']), 0, [], [])

    else:
        initList(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage)
    os.system("cat ./buffer/* > ./output.list && rm -f ./buffer/*")
    print("DONE : dictionary -> output.list")

#------------------------------------------------------------------------------------------#
