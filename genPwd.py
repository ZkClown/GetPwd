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
from utils.combine import processCombiner, processCombNext,initList
from os import getcwd, system, makedirs
from os.path import exists
import argparse

#------------------------------------------------------------------------------------------#




#----------------------------------Main----------------------------------------------------#

if __name__=="__main__":
    baseDir = getcwd()
    buffer = baseDir+"/buffer"
    if not exists(buffer):
        makedirs(buffer)
    #init lists
    wordList = []
    dateList = []
    garbage = []

    #init arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="file wich contains personals datas")
    ap.add_argument("-r", "--recurence", help="Number of iterations")
    ap.add_argument("-b", "--brute", help="Number of char to bruteforce if needed")
    ap.add_argument("-p", "--processes", help="Number of processes", default = 2)
    ap.add_argument("-d", "--difference", help="Don't combine two elements of one same set", action="store_true")
    args = vars(ap.parse_args())

    #loadCSV
    dico = loadCsv(baseDir+"/csv/leetTab.csv",";")
    dicoMonth = loadCsv(baseDir+"/csv/date.csv",";")
    dicoDepart = loadCsv(baseDir+"/csv/departements.csv", ";")
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
    
    try:
        nbProcess = int(args["processes"])
    except ValueError:
        print("[ERROR] give an integer value for parameter \"processes\"")

    #iterations
    if args["recurence"]:
        if args["recurence"] in "012":
            if int(args["recurence"]) > 0:
                if args["difference"]:
                    processCombiner(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage, 1, myWords, myDates, nbProcess)
                else:
                    processCombiner(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage, 0, [], [], nbProcess)
                if int(args["recurence"]) > 1:
                    if args["difference"]:
                        processCombNext(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage,int(args['recurence']), 1, myWords, myDates, nbProcess)
                    else:
                        processCombNext(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage,int(args['recurence']), 0, [], [], nbProcess)
           #else:
            #    initList(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage)

    else:
        initList(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage)

    #Last Packing
    system("/bin/cat "+buffer+"/* > "+baseDir+"/output.list && /bin/rm -f "+buffer+"/*")
    print("DONE : dictionary -> output.list")

#------------------------------------------------------------------------------------------#
