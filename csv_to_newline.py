#!/usr/bin/python3

import sys
import re
from os.path import exists

## comma seperated string
INPUT_FILE=sys.argv[1]

res=""


with open(INPUT_FILE) as file1:
    input_data=file1.read()


## generate a list out of comma seperated string
input_list=input_data.split(",")


for ip in input_list:
    if (res == ""):
        res = ip
    else:
        res = res + "\n" + ip

with open(INPUT_FILE, "w") as file2:
    file2.write(res)

