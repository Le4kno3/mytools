#!/usr/bin/python3

import sys
import re
from os.path import exists

## comma seperated string
INPUT_FILE=sys.argv[1]

## comman seperated string
ADD_FILE=sys.argv[2]

res=""


with open(INPUT_FILE) as file1:
    input_data=file1.read()

with open(ADD_FILE) as file2:
    add_data=file2.read()

## generate a list out of comma seperated string
input_list=input_data.split(",")

## generate a list out of comma seperated string
add_list=add_data.split(",")

count=0

for ip in add_list:
    if (ip not in input_list):
        count=count+1
        input_list.append(ip)

for ip in input_list:
    if (res == ""):
        res = ip
    else:
        res = res + "," + ip



## if no ip to add
if(count == 0):
    sys.exit("No IP added as all IPs already exists.")

## Check if active_targets.txt file already exists
if (exists(INPUT_FILE) && count > 0):
    print("===> Note: Adding" + count + " ips and overwritting " + INPUT_FILE + ".")
    with open(INPUT_FILE, "w") as file3:
        file3.write(res)
else:
    sys.exit("Either input file does not exists.")
