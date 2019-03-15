#!/usr/bin/python3
# -*- coding: utf-8 -*-




#----------------------------------Credits-------------------------------------------------#
#                                                                                          #
#                          Made by Squadella & ZkClown                                     #
#                                                                                          #
#------------------------------------------------------------------------------------------#




#----------------------------------Imports-------------------------------------------------#

from utils.utils import miniBf, loadPersonalsDatas, loadCsv, lolToSl, colors, garbageObject
from utils.wordsHandler import threadLauncher
from utils.datesHandler import threadDateLauncher, loadDatesWithSeparators
from utils.combine import processCombiner, processCombNext,initList
from os import getcwd, system, makedirs
from os.path import exists
import argparse

#------------------------------------------------------------------------------------------#




#----------------------------------Main----------------------------------------------------#

if __name__=="__main__":
    # Set buffer folder. Create it if not exists and rm the content.
    baseDir = getcwd()
    buffer = baseDir+"/buffer"
    if not exists(buffer):
        makedirs(buffer)
    system("/bin/rm -rf "+buffer+"/*")
    
    #init lists
    wordList = []
    dateList = []
    garbage = []

    #init arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="file wich contains personals datas")
    ap.add_argument("-r", "--recurence", help="Number of iterations")
    ap.add_argument("-b", "--brute", help="Number of char to bruteforce if needed")
    ap.add_argument("-c", "--charset", help="Charset used for the bruteforce")
    ap.add_argument("-p", "--processes", help="Number of processes", default = 2)
    ap.add_argument("-d", "--difference", help="Don't combine two elements of one same set", action="store_true")
    args = vars(ap.parse_args())

    #loadCSV
    dico = loadCsv(baseDir+"/csv/leetTab.csv",";")
    dicoMonth = loadCsv(baseDir+"/csv/date.csv",";")
    dicoDepart = loadCsv(baseDir+"/csv/departements.csv", ";")
    try:
        loadPersonalsDatas(loadCsv(args["file"], ";"), dateList, wordList)
    except Exception:
        print(colors.red+"[ERROR]: "+colors.rst+"File given doesn't exist or bad permissions")
        exit(1)
    #Generate all dates and leet
    myWords = threadLauncher(wordList, dico, dicoDepart)
    myDates = threadDateLauncher(dateList, dicoMonth)

    #brute force on 4 char
    if args["brute"]:
        try:
            print(args["charset"])
            miniBf("", garbage, int(args["brute"]), args["charset"])
        except ValueError:
            print(colors.red+"[ERROR]: "+colors.rst+"give an integer value for parameter \"brute\"")
            exit(1)
        myGarbage = [garbageObject(garbage)]

    try:
        nbProcess = int(args["processes"])
    except ValueError:
        print(colors.red+"[ERROR]: "+colors.rst+"give an integer value for parameter \"processes\"")
        exit(1)
    

    

    if args["recurence"]:
        try:
            recurence = int(args["recurence"])
        except ValueError:
            print(colors.red+"[ERROR]: "+colors.rst+"give an integer between 0 and 2 for parameter \"recurence\"")
            exit(1)
        
        if recurence >= 0 and recurence <= 2:
            if recurence > 0:
                if args["difference"]:
                    processCombiner(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage, 1, myWords, myDates,myGarbage, nbProcess)
                else:
                    processCombiner(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage, 0, [], [], [],nbProcess)
                if recurence > 1:
                    if args["difference"]:
                        processCombNext(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage,recurence, 1, myWords, myDates,myGarbage ,nbProcess)
                    else:
                        processCombNext(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage,recurence, 0, [], [],[] ,nbProcess)
            else:
                initList(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage)

        else:
            print(colors.red+"[ERROR]: "+colors.rst+"give an integer between 0 and 2 for parameter \"recurence\"")
            exit(1)

    else:
        initList(lolToSl(myWords)+loadDatesWithSeparators(myDates)+garbage)

    #Last Packing
    system("/bin/cat "+buffer+"/* > "+baseDir+"/output.list && /bin/rm -f "+buffer+"/*")
    print(colors.green+"DONE: "+colors.rst+"dictionary -> output.list")

#------------------------------------------------------------------------------------------#
