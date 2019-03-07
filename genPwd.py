#!/usr/bin/python3
# -*- coding: utf-8 -*-




#----------------------------------Credits-------------------------------------------------#
#                                                                                          #
#                          Made by Squadella & ZkClown                                     #
#                                                                                          #
#------------------------------------------------------------------------------------------#




#----------------------------------Imports-------------------------------------------------#

from utils.utils import miniBf, loadPersonalsDatas, loadCsv, lolToSl
from utils.wordsHandler import threadLauncher
from utils.datesHandler import threadDateLauncher, loadDatesWithSeparators
from utils.combine import threadCombiner, threadCombNext,initList
import argparse
import os

#------------------------------------------------------------------------------------------#




#----------------------------------Main----------------------------------------------------#

if __name__=="__main__":
    buffer = "./buffer"
    if not os.path.exists(buffer):
        os.makedirs(buffer)
    #init lists
    wordList = []
    dateList = []
    garbage = []

    #init arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="file wich contains personals datas")
    ap.add_argument("-r", "--recurence", help="Number of iterations")
    ap.add_argument("-b", "--brute", help="Number of char to bruteforce if needed")
    ap.add_argument("-d", "--difference", help="Don't combine two elements of one same set", action="store_true")
    args = vars(ap.parse_args())

    #loadCSV
    dico = loadCsv("./csv/leetTab.csv",";")
    dicoMonth = loadCsv("./csv/date.csv",";")
    dicoDepart = loadCsv("./csv/departements.csv", ";")
    loadPersonalsDatas(loadCsv(args["file"], ";"), dateList, wordList)

    #Generate all dates and leet
    myWords = threadLauncher(wordList, dico, dicoDepart)
    myDates = threadDateLauncher(dateList, dicoMonth)

    #brute force on 4 char
    if args["brute"]:
        try:
            miniBf("", garbage, int(args["brute"]))
        except ValueError:
            print("[ERROR] give an integer value for parameter \"brute\"")


    #iterations
    if args["recurence"]:
        if args["recurence"] in "012":
            if int(args["recurence"]) > 0:
                if args["difference"]: 
                    threadCombiner(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage, 1, myWords, myDates)
                else:
                    threadCombiner(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage, 0, [], [])
                if int(args["recurence"]) > 1:
                    if args["difference"] == "1":
                        threadCombNext(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage,int(args['recurence']), 1, myWords, myDates)
                    else:
                        threadCombNext(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage,int(args['recurence']), 0, [], [])
           #else:
            #    initList(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage)

    else:
        initList(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage)

    #Last Packing
    os.system("cat ./buffer/* > ./output.list && rm -f ./buffer/*")
    print("DONE : dictionary -> output.list")

#------------------------------------------------------------------------------------------#
