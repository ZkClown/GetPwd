#!/usr/bin/python3
# -*- coding: utf-8 -*-




#----------------------------------Credits-------------------------------------------------#
#                                                                                          #
#                          Made by Squadella & ZkClown                                     #
#                                                                                          #
#------------------------------------------------------------------------------------------#




#----------------------------------Imports-------------------------------------------------#

import os
from threading import Thread
import re

#------------------------------------------------------------------------------------------#




#----------------------------------Threads-------------------------------------------------#

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
    if(lastValue != len(list)-1):
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
        if(lastValue != len(list)-1):
            tmp.append(partCombNext(list, lastValue, len(list), threadNumber, diff, myWords, myDates))
        for thread in tmp:
            thread.start()
        print("Fin lancement thread")
        for thread in tmp:
            thread.join()
        print("Packing")
        os.system("cat ./buffer/*.txt > ./buffer/output"+str(j)+" && rm ./buffer/*.txt")

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
    for word in myWords:
        word.done2 = word.done
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
                    if j > len(list)-1:
                        break
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
    for date in myDates:
        date.convertDoneInList()
    for word in myWords:
        word.done2 = word.done
    flag = 0
    flag2 = 0
    numLine = 0
    pos = 0
    count = 0
    buff = []
    jump = 1
    file = open("./buffer/"+str(index).zfill(3)+".txt","w")
    if diff != 1:
        for i in range(startValue, endValue):
            file2 = open("./buffer/output", "r")
            for line in file2:
                file.write(list[i]+line)
    else:
        for i in range(startValue, endValue):
            file2 = open("./buffer/output", "r")
            for line in file2:
                if flag2 == 0:
                    if flag == 0:
                        buff = analyzeString(line[:-1], myWords, myDates)
                        for word in buff:
                            if list[i] in word[0].done2:
                                flag = 1
                                pos = word[1]
                                if pos == 0:
                                    numLine = count + len(word[0].done2)*(len(list)-len(word[0].done2)) - 1
                                else:
                                    numLine = count + len(word[0].done2) - 1
                                break
                        if flag == 0:
                            file.write(list[i]+line)
                            numLine = count + len(buff[-1][0].done2) - 1
                            flag2 = 1
                    else:
                        if count == numLine:
                            flag = 0
                else:
                    file.write(list[i]+line)
                    if count == numLine:
                        flag2 = 0


                count += 1
            count = 0
            file2.close()
    file.close()


def analyzeString(string, myWords, myDates):
    for date in myDates:
        date.convertDoneInList()
    for word in myWords:
        word.done2 = word.done
    res = []
    temp = []
    pos = 0
    for word in myWords+myDates:
        for x in word.done2:
            if x in string:
                temp.append([x,word])
                break
    while temp != []:
        for x in temp:
            if string[len(x[0]):] == re.sub(x[0], '', string):
                res.append([x[1],pos])
                pos+=1
                temp.remove(x)
                string = string[len(x[0]):]
                break
    return res


#------------------------------------------------------------------------------------------#
