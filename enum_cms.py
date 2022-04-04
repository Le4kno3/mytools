#!/usr/bin/python3

import sys
import re
import subprocess
from os.path import exists
import random

INPUT_FILE=sys.argv[1]          # input
OUTPUT_FILE=sys.argv[2]    # output

MYHOME="/home/ubuntu/Documents/synackfiles"

data=""
with open(INPUT_FILE, "r") as file1:
    data=file1.read()

lines=data[0:len(data)-1].split("\n")

results=""
for line in lines:
    cmd=MYHOME+"/tools/whatcms.sh "+line
    task = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    out = task.stdout.decode('utf-8')
    results = results + out + "\n"

# for line in lines:
#     cmd="/usr/bin/python3 "+MYHOME+"/tools/CMSeeK/cmseek.py -u "+line
#     print(cmd)
#     task = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
#     out = task.stdout.decode('utf-8')
#     results = results + out + "\n"

with open(OUTPUT_FILE, "w") as file1:
    file1.write(results)