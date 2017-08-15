# GetPwd

## Description
It's a tool which generate a dictionary from a csv containing personals informations.

Generate all common passwords based on perso info. (leet transformations and combinatory processing)

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
  - etc ....

## Usage
```
git clone project
genPwd.py [-h] -f FILE [-r RECURENCE] [-b BRUTE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file wich contains personals datas
  -r RECURENCE, --recurence RECURENCE
                        Number of iterations
  -b BRUTE, --brute BRUTE
                        Activate brute force, 1 to activate
```

## CSV format
The csv has to contain 1 info per line !
dates must have the following format : dd/mm/yyyy (01/12/2012)

## CAUTION

The more infos there are in the csv, the larger the dictionary will be ! Same for iterations !

## Credits
Made by [ZkClown](https://github.com/ZkClown) & [Squadella](https://github.com/Squadella)

[![Python 3|3.6](https://img.shields.io/badge/python-3%7C3.5-yellow.svg)](https://www.python.org/)
