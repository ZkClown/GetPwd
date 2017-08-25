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
cd ./GetPwd && mkdir ./buffer
genPwd.py [-h] -f FILE [-r RECURENCE] [-b BRUTE] [-d DIFFERENCE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file wich contains personals datas
  -r RECURENCE, --recurence RECURENCE
                        Number of iterations 0 to 2
  -b BRUTE, --brute BRUTE
                        Activate brute force, 1 to activate
  -d DIFFERENCE, --difference
                        Deactivate the re usage of a same info more than once, 1 to deactivate
```
## Exemple usage 

` genPwd.py -f myCsv.csv -r 2 -d 1 `
This will generate all possible passwords without the re-use of information and which can be composed of maximum 3 different informations 

## CSV format
The csv has to contain 1 info per line !
Dates must have the following format : dd/mm/yyyy (01/12/2012)

## CAUTION

The more infos there are in the csv, the larger the dictionary will be ! Same for iterations !

## Credits
Made by [ZkClown](https://github.com/ZkClown) & [Squadella](https://github.com/Squadella)

[![Python 3|3.6](https://img.shields.io/badge/python-3%7C3.6-yellow.svg)](https://www.python.org/)
