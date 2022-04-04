#!/usr/bin/python3

import sys
import re
import subprocess
from os.path import exists
import random

INPUT_FILE=sys.argv[1]          # output from gospider
OUTPUT_FILE_BASE=sys.argv[2]    #$MYHOME/targets/$TARGETS/notes

MYHOME="/home/csoc_user/MyData/synackfiles"

# Example
# /usr/bin/python3 /home/csoc_user/MyData/synackfiles/tools/categorize_crawled_results.py /home/csoc_user/MyData/synackfiles/targets/FOODO/logs/gospider_crawl_30-03-2022-13_50_46.log/ec-www_stg_rds-platform_io /home/csoc_user/MyData/synackfiles/targets/FOODO/notes

data=""
with open(INPUT_FILE) as file1:
    data=file1.read()

with open(OUTPUT_FILE_BASE+"/crawled_urls.txt") as file1:
    data=data+file1.read()

# Create js.txt
# pattern=r"\[javascript\] - .*"
pattern=r".*?\.js$"
matches = re.finditer(pattern, data, re.MULTILINE)
js_data=""
for matchNum, match in enumerate(matches, start=1):
    tmp=re.sub(r"\[javascript\] - ","",match.group(),0,re.MULTILINE)
    js_data=js_data+tmp+"\n"

with open(OUTPUT_FILE_BASE+"/js.txt", "w") as file_tmp:
    file_tmp.write(js_data)


# Create subdomains.txt
pattern=r"\[subdomains\] - .*"
matches = re.finditer(pattern, data, re.MULTILINE)
subdomain_data=""
for matchNum, match in enumerate(matches, start=1):
    tmp=re.sub(r"\[subdomains\] - ","",match.group(),0,re.MULTILINE)
    subdomain_data=subdomain_data+tmp+"\n"

with open(OUTPUT_FILE_BASE+"/subdomains.txt", "w") as file_tmp:
    file_tmp.write(subdomain_data)


# Create api.txt
pattern=r".*?api.*"
matches = re.finditer(pattern, data, re.MULTILINE)
api_data=""
for matchNum, match in enumerate(matches, start=1):
    # print(match.group())
    tmp=re.sub(r".*? - ","",match.group(),0,re.MULTILINE)
    print(tmp)
    # if tmp.find("fonts.googleapis.com") != -1:
    if "fonts.googleapis.com" not in tmp:
        api_data=api_data+tmp+"\n"

with open(OUTPUT_FILE_BASE+"/api.txt", "w") as file_tmp:
    # print(api_data)
    file_tmp.write(api_data)



