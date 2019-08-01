# GetPwd

## Description
It's a tool which generates a dictionary from a csv containing personal informations.

Generates all common passwords based on perso info. (leet transformations and combinatory processing)

The purpose of the script is to test the usage of weak passwords.

The script is written in PYTHON 3
## Exemple

### Personnals infos :
  - Name : Jean
  - Surname : Dupont
  - Date of birth : 20th June 1988

### Pwd Generated :
  - JeanDupont
  - Jean
  - jean
  - j3an
  - j34n
  - J34n
  - Je4n200688
  - etc ....

## Usage
```
git clone https://github.com/ZkClown/GetPwd.git
cd ./GetPwd
python getPwd.py -h
usage: getPwd.py [-h] -f FILE [-r RECURENCE] [-b BRUTE] [-c CHARSET]
                 [-o OUTPUT] [-p PROCESSES] [-d] [-l LEET]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file wich contains personals datas
  -r RECURENCE, --recurence RECURENCE
                        Number of combinations
  -b BRUTE, --brute BRUTE
                        Number of char to bruteforce if needed
  -c CHARSET, --charset CHARSET
                        Charset used for the bruteforce
  -o OUTPUT, --output OUTPUT
                        Output file
  -p PROCESSES, --processes PROCESSES
                        Number of processes
  -d, --difference      Don't combine two elements of one same set
  -l, --leet            Use leet table instead of only Maj and Min
```
## Exemple usage 

` genPwd.py -f myCsv.csv -r 2 -d -b 2 -c "abc" -p 4 -o out`

This will generate all possible passwords without the re-use of information with garbages chars using the charset "abc" up to 3 chars and which can be composed of maximum 3 different informations. 

## CSV format
The csv has to contain 1 info per line !

## CAUTION

The more infos there are in the csv, the larger the dictionary will be ! Same for combinations !

## Credits
Made by [ZkClown](https://github.com/ZkClown) & [Squadella](https://github.com/Squadella)

[![Python 3|3.6](https://img.shields.io/badge/python-3%7C3.6-yellow.svg)](https://www.python.org/)
