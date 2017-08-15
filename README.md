# GetPwd

## Description
It's a tool which generate a dictionary from a csv containing personals informations.

Generate all common password based on perso info. (leet transformations and combinatory processing)

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

## Credits
Made by [ZkClown](https://github.com/ZkClown) & [Squadella](https://github.com/Squadella)
