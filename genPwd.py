#!/usr/bin/python3
# -*- coding: utf-8 -*-




#----------------------------------Credits-------------------------------------------------#
#                                                                                          #
#                          Made by Squadella & ZkClown                                     #
#                                                                                          #
#------------------------------------------------------------------------------------------#




#----------------------------------Imports-------------------------------------------------#

from utils.utils import *
from utils.wordsHandler import *
from utils.datesHandler import *
from utils.combine import *
import argparse
import os

#------------------------------------------------------------------------------------------#




#----------------------------------Main----------------------------------------------------#

if __name__=="__main__":

    #init lists
    wordList = []
    dateList = []
    garbage = []

    #init arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="file wich contains personals datas")
    ap.add_argument("-r", "--recurence", help="Number of iterations")
    ap.add_argument("-b", "--brute", help="Activate brute force, 1 to active")
    ap.add_argument("-d", "--difference", help="Activate the re usage of a same info more than once, 1 to activate")
    arg = ap.parse_args()
    args = vars(ap.parse_args())

    #loadCSV
    dico = loadCsv("./csv/leetTab.csv",";")
    dicoMonth = loadCsv("./csv/date.csv",";")
    loadPersonalsDatas(loadCsv(args["file"], ";"), dateList, wordList)

    #Generate all dates and leet
    myWords = threadLauncher(wordList, dico)
    myDates = threadDateLauncher(dateList, dicoMonth)

    #brute force on 4 char
    if arg.brute:
        if args["brute"] == "1":
            miniBf("", garbage)

    #iterations
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

    #Last Packing 
    os.system("cat ./buffer/* > ./output.list && rm -f ./buffer/*")
    print("DONE : dictionary -> output.list")

#------------------------------------------------------------------------------------------#
