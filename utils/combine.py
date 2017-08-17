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
