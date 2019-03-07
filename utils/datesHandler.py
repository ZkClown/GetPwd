#!/usr/bin/python3
# -*- coding: utf-8 -*-




#----------------------------------Credits-------------------------------------------------#
#                                                                                          #
#                          Made by Squadella & ZkClown                                     #
#                                                                                          #
#------------------------------------------------------------------------------------------#




#----------------------------------Imports-------------------------------------------------#

import datetime
from threading import Thread
import itertools

#------------------------------------------------------------------------------------------#




#----------------------------------Classes-------------------------------------------------#

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
        elif len(date.split('/')) == 2:
            if len(date.split('/')[1]) != 4:
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
                self.year = 0
            else:
                self.day = 0
                self.month = date.split('/')[0]
                self.year = [date.split('/')[1], date.split('/')[1][2:]]

        else:
            self.month = 0
            self.day = 0
            self.year = [date, date[2:]]
        self.done = []
        self.done2 = []

    #Generate all differents formats for a given date : d-m-y (little endian)/ m-d-y (middle endian)/ y-m-d (big endian)
    def genDatesFormat(self, dictionary):
        if self.month != 0:
            self.month = self.month.split(' ') #Transform string in list of strings
            for month in dictionary:
                if self.month[0] in month:
                    self.month = month
                    break
        if self.year != 0:
            if self.month != 0 and self.day != 0:
                temp = [self.day, self.month, self.year]
                temp2 = [self.month, self.day, self.year]
                temp3 = [self.year, self.month, self.day]

                temp4 = [self.day, self.month]
                temp5 = [self.month, self.day]

                temp6 = [self.month, self.year]
                temp7 = [self.year, self.month]

                temp = list(itertools.product(*temp))
                temp2 = list(itertools.product(*temp2))
                temp3 = list(itertools.product(*temp3))

                temp4 = list(itertools.product(*temp4))
                temp5 = list(itertools.product(*temp5))

                temp6 = list(itertools.product(*temp6))
                temp7 = list(itertools.product(*temp7))
                for x in temp2:
                    temp.append(x)
                for x in temp3:
                    temp.append(x)

                for x in temp4:
                    temp.append(x)
                for x in temp5:
                    temp.append(x)

                for x in temp6:
                    temp.append(x)
                for x in temp7:
                    temp.append(x)

                temp.append([self.year[0]])
                temp.append([self.year[1]])

            elif self.month == 0 and self.day == 0:
                temp = []
                temp.append([self.year[0]])
                temp.append([self.year[1]])

            else:
                temp = [self.month, self.year]
                temp2 = [self.year, self.month]

                temp = list(itertools.product(*temp))
                temp2 = list(itertools.product(*temp2))

                for x in temp2:
                    temp.append(x)

        else:
            temp = [self.day, self.month]
            temp2 = [self.month, self.day]
            temp = list(itertools.product(*temp))
            temp2 = list(itertools.product(*temp2))
            for x in temp2:
                temp.append(x)
        self.done = temp

    def convertDoneInList(self):
        res = [self]
        self.done2 = loadDatesWithSeparators(res)

    def reasignDone(self,list):
        self.done = list

#------------------------------------------------------------------------------------------#




#----------------------------------Threads-------------------------------------------------#

#Thread to generate dates format for all dates
class genDates(Thread):
    def __init__(self, date, dictionary):
        Thread.__init__(self)
        self.word = date
        self.dictionary = dictionary
        super(genDates, self).__init__()

    def run(self):
        self.word.genDatesFormat(self.dictionary)

#------------------------------------------------------------------------------------------#




#----------------------------------Thread Launchers----------------------------------------#

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

#------------------------------------------------------------------------------------------#




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
