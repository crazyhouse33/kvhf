#!/usr/bin/python3
#read the content of devignore file and compare it to to sys[1] to know if the file is to be ignored
import sys
import re

#arg checks and recup
if len(sys.argv)!=2:
    sys.exit(0)
theFile= sys.argv[1]
toIgnore= False

#getting the ignore file
with open("dev/devignore",'r') as f:
    regexplist=f.read().splitlines()

# atctions
for reg in regexplist:
    try:
        firstchar= reg[0]
    except:#empty string
        continue 

    if firstchar=='#': #comment
        continue

    elif firstchar=='!': #include
        if re.match(reg[1:], theFile):
            print(0)
            sys.exit(0)

    else :#exclude
        if re.match (reg, theFile):
            toIgnore=True
if toIgnore:
    print(1)
else :
    print (0)
sys.exit(0)

