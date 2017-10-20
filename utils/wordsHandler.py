#!/usr/bin/python3
# -*- coding: utf-8 -*-




#----------------------------------Credits-------------------------------------------------#
#                                                                                          #
#                          Made by Squadella & ZkClown                                     #
#                                                                                          #
#------------------------------------------------------------------------------------------#




#----------------------------------Imports-------------------------------------------------#

from threading import Thread

#------------------------------------------------------------------------------------------#




#----------------------------------Classes-------------------------------------------------#

#Class to generate Leet from a word
class word:
    #Initialisation
    def __init__(self, word):
        temp = ""
        for i in word:
            if i.isalpha():
                temp += i
        self.word = temp
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

    def departmentsCorres(self, dictionary):
        for depart in dictionary:
            if self.word.lower() == depart[1].lower():
                for i in depart:
                    if not self.word.lower() == i.lower():
                        self.done.append(i)


#------------------------------------------------------------------------------------------#




#----------------------------------Threads-------------------------------------------------#

#Thread to generate leet for all words in personal infos
class genObjects(Thread):
    def __init__(self, word, dictionary, departements):
        Thread.__init__(self)
        self.word = word
        self.dictionary = dictionary
        self.departements = departements
        super(genObjects, self).__init__()

    def run(self):
        self.word.genWords(self.dictionary, "", 0)
        self.word.departmentsCorres(self.departements)

#------------------------------------------------------------------------------------------#




#----------------------------------Thread Launchers----------------------------------------#

def threadLauncher(wordList,dictionary, departements):
    myWords = []
    temp = []
    for wordInList in wordList:
        myWords.append(word(wordInList))
    for i in myWords:
        temp.append(genObjects(i, dictionary, departements))
    for thread in temp:
        thread.start()
    for thread in temp:
        thread.join()

    return myWords

#------------------------------------------------------------------------------------------#
