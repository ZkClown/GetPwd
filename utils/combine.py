#!/usr/bin/python3
# -*- coding: utf-8 -*-




#----------------------------------Credits-------------------------------------------------#
#                                                                                          #
#                          Made by Squadella & ZkClown                                     #
#                                                                                          #
#------------------------------------------------------------------------------------------#




#----------------------------------Imports-------------------------------------------------#

from os import system, getcwd
from multiprocessing import Process
from re import sub

#------------------------------------------------------------------------------------------#




#----------------------------------Processs-------------------------------------------------#

class partCombine(Process):
    def __init__(self,list, begValue, end, index, diff, myWords, myDates):
        Process.__init__(self)
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

class partCombNext(Process):
    def __init__(self,list, begValue, end, index, diff, myWords, myDates):
        Process.__init__(self)
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




#----------------------------------Process Launchers----------------------------------------#

def processCombiner(list, diff, myWords, myDates, nbProcess):
    baseDir = getcwd()
    initList(list)
    lastValue = 0
    processNumber = 1
    step = int(len(list)/nbProcess)
    tmp = []
    for i in range(1,len(list)):
        if(i%step == 0):
            tmp.append(partCombine(list, lastValue, i, processNumber, diff, myWords, myDates))
            lastValue = i
            processNumber += 1
    if(lastValue != len(list)-1):
        tmp.append(partCombine(list, lastValue, len(list), processNumber, diff, myWords, myDates))
    for process in tmp:
        process.start()
    print("Processes Launched")
    for process in tmp:
        process.join()
    print("Packing")
    system("/bin/cat "+baseDir+"/buffer/*.txt > "+baseDir+"/buffer/output && /bin/rm "+baseDir+"/buffer/*.txt")

def processCombNext(list, rec, diff, myWords, myDates, nbProcess):
    baseDir = getcwd()
    for j in range(1,rec):
        lastValue = 0
        processNumber = 0
        step = int(len(list)/nbProcess)
        tmp = []
        for i in range(1,len(list)):
            if(i%step == 0):
                tmp.append(partCombNext(list, lastValue, i, processNumber, diff, myWords, myDates))
                lastValue = i
                processNumber += 1
        if(lastValue != len(list)-1):
            tmp.append(partCombNext(list, lastValue, len(list), processNumber, diff, myWords, myDates))
        for process in tmp:
            process.start()
        print("Processes Launched")
        for process in tmp:
            process.join()
        print("Packing")
        system("/bin/cat "+baseDir+"/buffer/*.txt > "+baseDir+"/buffer/output"+str(j)+" && /bin/rm "+baseDir+"/buffer/*.txt")

#------------------------------------------------------------------------------------------#




#----------------------------------Writing-------------------------------------------------#

def initList(list):
    baseDir = getcwd()
    file = open(baseDir+"/buffer/000","w")
    for word in list:
        file.write(word+"\n")
    file.close()

def packing(list, start, end, index, diff , myWords, myDates):
    baseDir = getcwd()
    for date in myDates:
        date.convertDoneInList()
    for word in myWords:
        word.done2 = word.done
    flag2 = 0
    j = 0
    temp = ""
    file = open(baseDir+"/buffer/"+str(index).zfill(3)+".txt","w")
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
    baseDir = getcwd()
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
    file = open(baseDir+"/buffer/"+str(index).zfill(3)+".txt","w")
    if diff != 1:
        for i in range(startValue, endValue):
            file2 = open(baseDir+"/buffer/output", "r")
            for line in file2:
                file.write(list[i]+line)
    else:
        for i in range(startValue, endValue):
            file2 = open(baseDir+"/buffer/output", "r")
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
            if string[len(x[0]):] == sub(x[0], '', string):
                res.append([x[1],pos])
                pos+=1
                temp.remove(x)
                string = string[len(x[0]):]
                break
    return res


#------------------------------------------------------------------------------------------#
