#!/usr/bin/python3
# Python program designed only for aquatone tool, others will notwork.

import sys 
import json
import csv
import re

if ( sys.argv[1] == "" ):
    sys.extit("Provide the TARGET name inline.")

MYHOME="/home/AMBERJACK/fg8f7yz1uq/Documents/synackfiles"
TARGET=sys.argv[1]
JSON_FILEPATH = MYHOME+"/targets/"+TARGET+"/screenshots/aquatone_session.json"
CSV_FILEPATH = MYHOME+"/targets/"+TARGET+"/screenshots/aquatone_session.csv"

data={}

# Opening JSON file
with open(JSON_FILEPATH) as file1:
    data = json.load(file1)    # returns JSON object to dict


with open(CSV_FILEPATH, 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Sr.', 'URL', 'Status Code', 'Title', 'Attackable' ,'ScreenshotCaptured'])
    count=1
    for key in data['pages'].keys():
        #to ensure csv is adhered
        title=data['pages'][key]['pageTitle']
        title=re.sub(r",","(comma)",title,0,re.MULTILINE)
        
        #writing data in csv file
        filewriter.writerow([count, data['pages'][key]['url'], data['pages'][key]['status'], title, "todo",data['pages'][key]['hasScreenshot']])
        count=count+1