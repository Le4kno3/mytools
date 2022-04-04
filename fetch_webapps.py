#!/usr/bin/python3

import sys
import re
import subprocess
from os.path import exists
import random

INPUT_FILE=sys.argv[1]
OUTPUT_FILE=sys.argv[2]

## only for httprobe
THREADS="10"

MYHOME="/home/AMBERJACK/fg8f7yz1uq/Documents/synackfiles"

res=""

datalist=[]


with open(INPUT_FILE) as file1:
    data=file1.read()


pattern=r"^Nmap scan report for [\S\s]*?\n\n"

matches = re.finditer(pattern, data, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    datalist.append(match.group())


#fetch ip and ports
for data in datalist:
    ip=""
    pattern=r"\b(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b[^\.]"
    matches = re.finditer(pattern, data, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        ip=re.sub(r"\)","",match.group(),0,re.MULTILINE)
        ip=re.sub("\n","",ip,0,re.MULTILINE)

    ports=[]
    pattern=r"\b[0-9]*?/"
    matches1 = re.finditer(pattern, data, re.MULTILINE)
    for matchNum, match in enumerate(matches1, start=1):
        port=re.sub(r"/","",match.group(),0,re.MULTILINE)
        ports.append(port)

    for port in ports:
        tmp=ip + ":" + port
        if (res == ""):
          res = tmp
        else:
            res = res + "\n" + tmp 


## create a temp file
with open("/tmp/rough", "w") as file_tmp:
    file_tmp.write(res)


## reset res variable
res=""

cmd="cat /tmp/rough | " + MYHOME + "/tools/httprobe -c "+THREADS

task = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = task.stdout.read()
assert task.wait() == 0


## convert from byte to string
out = out.decode("utf-8")
# out=re.sub(r"\n","",out,0,re.MULTILINE)
# print(out)

res = out

# print(res)


## Halt if active_targets.txt file already exists
if (exists(OUTPUT_FILE)):
    TMPFILE = OUTPUT_FILE+str(random.randint(100, 999))
    with open(TMPFILE, "w") as file4:
        file4.write(res)
    sys.exit("Warning: Ouput file 'active_webapps.txt' already exists. Create a new file, "+TMPFILE)

with open(OUTPUT_FILE, "w") as file2:
    file2.write(res)
