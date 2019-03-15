#!/usr/bin/python3
# -*- coding: utf-8 -*-




#----------------------------------Credits-------------------------------------------------#
#                                                                                          #
#                          Made by Squadella & ZkClown                                     #
#                                                                                          #
#------------------------------------------------------------------------------------------#




#----------------------------------Imports-------------------------------------------------#

import csv

#------------------------------------------------------------------------------------------#




#----------------------------------Utils---------------------------------------------------#

# Colors for the outputs
class colors(object):
    red   = "\033[1;32;31m"
    green = "\033[1;32;32m"
    rst   = "\033[1;32;0m"

class garbageObject:
    #Initialisation
    def __init__(self, myList):
        self.done2 = myList

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

#Generate all possible strings from 1 char to lenWill char (BF)
def miniBf(string, list, lenWill, charset):
    res = ""
    if not charset: 
        dico = r"0123456789@&!:;,?./\\$*+-_=%€()[]|#\{\}"
    else:
        dico = charset
    if len(string)<lenWill:
        for char in dico:
            res = string + char
            list.append(res)
            miniBf(res, list, lenWill, charset)

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#------------------------------------------------------------------------------------------#




#----------------------------------Loading Csv----------------------------------------------#

def loadPersonalsDatas(dictionary, dateList, wordList): #dateList must be empty
    for entry in dictionary:
        if entry[0].count('/') > 0:
            dateList.append(entry[0])
        else:
            if(RepresentsInt(entry[0])):
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

#------------------------------------------------------------------------------------------#
