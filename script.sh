#!/bin/bash

#variables
server_name=$(hostname)
THREADS="4"
RATE="2"	#packets per second
TARGET=$1
PROD="no"
MYHOME="$HOME/MyData/synackfiles"
EXTENSIONS="" #CSV format


# Colors
# https://misc.flogisoft.com/bash/tip_colors_and_formatting
green='\e[32m'
blue='\e[34m'
blue='\e[34m'
red='\e[91m'
clear='\e[0m'
light_cyan='\e[96m'
light_yellow='\e[93m'
ColorGreen(){
	echo -ne $green$1$clear
}
ColorBlue(){
	echo -ne $blue$1$clear
}
ColorLightCyan(){
	echo -ne $light_cyan$1$clear
}
ColorLightYellow(){
	echo -ne $light_yellow$1$clear
}
ColorRed(){
	echo -ne $red$1$clear
}

# helper functions


# functions
function pingSweep() {
	output_file="${MYHOME}/targets/${TARGET}/logs/nmap_pingSweep_$(date +%d-%m-%Y-%H_%M_%S).log"
	input_file="${MYHOME}/targets/${TARGET}/targets.txt"
	query_pingSweep="nmap -sP --max-rate ${RATE} -iL ${input_file} -oN output_file ${output_file}"
	echo ""
	echo "$(ColorLightYellow '=======> Executing Ping Sweep <=======')"
	echo "command: "$(ColorLightCyan "${query_pingSweep}")
	echo ""
	echo -ne "$(ColorRed 'Execute the command (yes/no):')"
	read response
	
	if [[ $response == "yes" ]]
	then
		$query_pingSweep
	fi

	## After the scan is completed, then process this.
	cmd1_input=${output_file}
	cmd1_output="${MYHOME}/targets/${TARGET}/active_targets.txt"

	### This will fetch all IPs and create a new file named "active_targets.txt"

	cmd1="/usr/bin/python3 ${MYHOME}/tools/fetch_ip.py ${cmd1_input} ${cmd1_output}"
	echo ""
	echo "Executing command: "$(ColorLightCyan "${cmd1}")
	$cmd1
}

function webScanQuick() {
	output_file="${MYHOME}/targets/${TARGET}/logs/nmap_webQuick_$(date +%d-%m-%Y-%H_%M_%S).log"
	input_file="${MYHOME}/targets/${TARGET}/active_targets.txt"
	query_webQuick="nmap -Pn -sS -p $(cat $MYHOME/wordlists/ports-web-quick.txt) --max-rate ${RATE} -iL ${input_file} -oN ${output_file} --open"
	echo ""
	echo "$(ColorLightYellow '=======> Executing Web Port Scan Quick <=======')"
	echo "command: "$(ColorLightCyan "${query_webQuick}")
	echo ""
	echo -ne "$(ColorRed 'Execute the command (yes/no):')"
	read response
	
	if [[ $response == "yes" ]]
	then
		$query_webQuick
	fi

	## After the scan is completed, then process httprobe to find active webapps.
	cmd1_input=${output_file}
	cmd1_output="${MYHOME}/targets/${TARGET}/active_webapps.txt"
	### This will check all for all active webapps and print in 'active_webapps.txt' file
	cmd1="/usr/bin/python3 ${MYHOME}/tools/fetch_webapp.py ${cmd1_input} ${cmd1_output}"
	echo ""
	echo "Executing command: "$(ColorLightCyan "${cmd1}")
	$cmd1

	## Then, run aquatone
	cmd2_input="${MYHOME}/targets/${TARGET}/active_webapps.txt"
	cmd2_output="${MYHOME}/targets/${TARGET}/screenshots/"
	### This is needed for piped command execution
	data=$(cat ${cmd2_input})
	cmd2="${MYHOME}/tools/aquatone -out ${cmd2_output} -threads ${THREADS} -scan-timeout 500"
	echo ""
	echo "Executing command: "$(ColorLightCyan "${cmd2}")
	### Piped command inside bash script
	printf '%s\n' "${data}" | $cmd2 

	## Generate CSV format of data
	### This will check all for all active webapps and print in 'active_webapps.txt' file
	cmd3="/usr/bin/python3 ${MYHOME}/tools/json_to_csv.py ${TARGET}"
	echo ""
	echo "Executing command: "$(ColorLightCyan "${cmd3}")
	$cmd3
}


function findingWebpages() {
	extension_wordlist="$MYHOME/wordlists/web/web-extensions.txt"
	file_directory_wordlist="$MYHOME/wordlists/web/raft-medium-lowercase.txt"
	echo -ne "Do you know which extensions are used (yes/no): "
	read response
	
	if [[ $response == "yes" ]]
	then
		echo "Below is list of all probable extensions: "
		echo "asp,aspx,bat,c,cfm,cgi,css,com,dll,exe,htm,html,inc,jhtml,js,jsa,jsp,log,mdb,nsf,pcap,php,php2,php3,php4,php5,php6,php7,phps,pht,phtml,pl,reg,sh,shtml,sql,swf,txt,xml"
		echo -ne "Give a list of Probable Extensions (csv format): "
		read EXTENSIONS
	else
		tmp="${MYHOME}/tools/aquatone -out ${cmd2_output} -threads ${THREADS} -scan-timeout 500"
		ext_list=$(sed -z 's/\n/\,/g; s/\.//g' $extension_wordlist)
		ext_list=${ext_list::-1}
		EXTENSIONS=$ext_list
	fi

	## Create a file with list of all blank webpages.
	
	## BURPSUITE MUST BE STARTED ON DEFAULT PORTS.
	## Finding Extension (if possible)
	index_wordlist="${MYHOME}/wordlists/web/web-index-file.txt"
	cmd1="${MYHOME}/tools/feroxbuster --url https://180.167.229.181:443 --wordlist ${index_wordlist} --threads 1 --scan-limit 4 --extensions ${EXTENSIONS} --rate-limit 8 --burp"
	echo ""
	echo "Executing command: "$(ColorLightCyan "${cmd1}")
	$cmd1

	## Directory Bruteforcing
	cmd2="${MYHOME}/tools/feroxbuster --url https://180.167.229.181:443 --wordlist ${index_wordlist} --threads 1 --scan-limit 4 --rate-limit 8 --burp"
	echo ""
	echo "Executing command: "$(ColorLightCyan "${cmd2}")
	$cmd2

	## File Bruteforcing with possible Extension (for all identified directories including "/")
	cmd3="${MYHOME}/tools/feroxbuster --url https://180.167.229.181:443 --wordlist ${index_wordlist} --threads 1 --scan-limit 4 --extensions ${EXTENSIONS} --rate-limit 8 --burp"
	echo ""
	echo "Executing command: "$(ColorLightCyan "${cmd3}")
	$cmd3
}

function crawlWebapps() {
	output_file="${MYHOME}/targets/${TARGET}/logs/gospider_crawl_$(date +%d-%m-%Y-%H_%M_%S).log"
	input_file="${MYHOME}/targets/${TARGET}/active_webapps.txt"
	echo -ne "What should be the threads (default=10): "
	read tmp_threads
	if [[ $tmp_threads == '' ]]	#if no input then default=10
	then
		tmp_threads=10
	fi
	echo -ne "What should be the depth (default=3): "
	read tmp_depth
	if [[ $tmp_depth == '' ]]	#if no input then default=3
	then
		tmp_depth=3
	fi
	cmd1="${MYHOME}/tools/gospider -S ${input_file} -o ${output_file} -c ${tmp_threads} -d ${tmp_depth} -q"
	echo ""
	echo "$(ColorLightYellow '=======> Executing Gospider Crawling <=======')"
	echo ""
	echo "Executing command: "$(ColorLightCyan "${cmd1}")
	$cmd1
	
	echo -ne "(Task) Now manually copy the gospider output to /notes/crawled_urls.txt. Type Enter once done..."
	read somedata

	cmd2_input="${MYHOME}/targets/${TARGET}/notes/crawled_urls.txt"
	cmd2_outut_base="${MYHOME}/targets/${TARGET}/notes/"	#api.txt, subdomains.txt, js.txt
	# collect all crawled links to crawled_urls.txt and categorize data in /target/notes/
	cmd2="/usr/bin/python3 ${MYHOME}/tools/categorize_crawl_results.py ${cmd2_input} ${cmd2_output_base}"
	echo ""
	echo "$(ColorLightYellow '=======> Arranging Crawled Output <=======')"
	echo ""
	echo "Executing command: "$(ColorLightCyan "${cmd2}")
	$cmd2
}

function fetchInteresting() {
	echo -ne "Fetch links present in JS files (yes/no): "
	read usr_input
	if [[ $usr_input == "yes" ]]
	then
		cmd1_output="${MYHOME}/targets/${TARGET}/notes/links_to_review.txt"
		cmd1_input="${MYHOME}/targets/${TARGET}/notes/js.txt"
		cmd1="/usr/bin/python3 ${MYHOME}/tools/fetch_links.py ${cmd1_input} ${cmd1_output}"
		echo ""
		echo "$(ColorLightYellow '=======> Fetching links inside JS Files <=======')"
		echo ""
		echo "Executing command: "$(ColorLightCyan "${cmd1}")
		$cmd1
		# printf '%s\n' "${data}" | $cmd2 > $cmd1_output	#"${cmd2}" was not working
	fi

	# echo -ne "Fetch APIs (yes/no): "
}

function enumCMS() {
	cmd1_output="${MYHOME}/targets/${TARGET}/logs/enumCMS.logs"
	cmd1_input="${MYHOME}/targets/${TARGET}/notes/subdomains.txt"
	cmd1="/usr/bin/python3 ${MYHOME}/tools/enum_cms.py ${cmd1_input} ${cmd1_output}"
	echo ""
	echo "$(ColorLightYellow '=======> Finding CMS <=======')"
	echo ""
	echo "Executing command: "$(ColorLightCyan "${cmd1}")
	$cmd1
}

menu(){
echo -ne "
Script Main Menu
$(ColorGreen '1)') Ping Sweep (ouput=active_hosts.txt)
$(ColorGreen '2)') Web Scan Quick (ouput=active_webapps.txt)
$(ColorGreen '3)') Crawl All Active Webapps
$(ColorGreen '4)') Bruteforce files and directories to find webpages
$(ColorGreen '5)') JS Linkfinder
$(ColorGreen '6)') Enumerate CMS
$(ColorGreen '0)') Exit
$(ColorBlue 'Choose an option:') "
    read a
    case $a in
        1) pingSweep ; menu ;;
        2) webScanQuick ; menu ;;
		3) crawlWebapps ; menu ;;
		4) findingWebpages ; menu ;;
		5) fetchInteresting ; menu ;;
		6) enumCMS ; menu ;;
		0) exit 0 ;;
		*) echo -e $red"Wrong option."$clear; WrongCommand;;
    esac
}


echo -ne "Is the Target in production (yes/no/custom): "
read PROD
if [[ $PROD == "custom" ]]
then
	echo -ne "Enter custom threads count: "
	read THREADS
	echo -ne "Enter custom number of packets per second: "
	read RATE
	echo "Script will scan using \"${THREADS}\" parallel threads and \"${RATE}\" packets per second rate."	
elif [[ $PROD == "yes" ]]
then
	THREADS="1"
	RATE="2"
else
	THREADS="4"
	RATE="2"
fi

#calling menu function now
menu