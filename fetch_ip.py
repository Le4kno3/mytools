#!/usr/bin/python3

import sys
import re
from os.path import exists

INPUT_FILE=sys.argv[1]
OUTPUT_FILE=sys.argv[2]
res=""


with open(INPUT_FILE) as file1:
    data=file1.read()


pattern=r"\b(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b[^\.]"

matches = re.finditer(pattern, data, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    #print(match.group())
    tmp=re.sub(r"\)","",match.group(),0,re.MULTILINE)
    tmp=re.sub(r"\n","",tmp,0,re.MULTILINE)
    if (res == ""):
        res = tmp
    else:
        res = res + "\n" + tmp 


## Check if active_targets.txt file already exists
if (exists(OUTPUT_FILE)):
    sys.exit("ERROR: Ouput file 'active_targets.txt' already exists.")

file2=open(OUTPUT_FILE, "w")
file2.write(res)
