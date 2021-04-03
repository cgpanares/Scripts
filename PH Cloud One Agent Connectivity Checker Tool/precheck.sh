#!/bin/bash

# Pre-requirements

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo You are not running as the root user.  Please try again with root privileges.;
    logger -t You are not running as the root user.  Please try again with root privileges.;
    exit 1;
fi;

# Detect Linux platform
platform='';  # platform for requesting package
runningPlatform='';   # platform of the running machine
majorVersion='';
platform_detect() {
 isRPM=1
 if !(type lsb_release &>/dev/null); then
    distribution=$(cat /etc/*-release | grep '^NAME' );
    release=$(cat /etc/*-release | grep '^VERSION_ID');
 else
    distribution=$(lsb_release -i | grep 'ID' | grep -v 'n/a');
    release=$(lsb_release -r | grep 'Release' | grep -v 'n/a');
 fi;
 if [ -z "$distribution" ]; then
    distribution=$(cat /etc/*-release);
    release=$(cat /etc/*-release);
 fi;

 releaseVersion=${release//[!0-9.]}
 case $distribution in
     *"Debian"*)
        platform='Debian_'; isRPM=0; runningPlatform=$platform;
        if [[ $releaseVersion =~ ^7.* ]]; then
           majorVersion='7';
        elif [[ $releaseVersion =~ ^8.* ]]; then
           majorVersion='8';
        elif [[ $releaseVersion =~ ^9.* ]]; then
           majorVersion='9';
        elif [[ $releaseVersion =~ ^10.* ]]; then
           majorVersion='10';
        fi;
        ;;

     *"Ubuntu"*)
        platform='Ubuntu_'; isRPM=0; runningPlatform=$platform;
        if [[ $releaseVersion =~ ^14.* ]]; then
           majorVersion='14.04';
        elif [[ $releaseVersion =~ ^16.* ]]; then
           majorVersion='16.04';
        elif [[ $releaseVersion =~ ^18.* ]]; then
           majorVersion='18.04';
		elif [[ $releaseVersion =~ ^20.* ]]; then
			majorVersion='20.04';
        fi;
        ;;

     *"SUSE"* | *"SLES"*)
        platform='SuSE_'; runningPlatform=$platform;
        if [[ $releaseVersion =~ ^11.* ]]; then
           majorVersion='11';
        elif [[ $releaseVersion =~ ^12.* ]]; then
           majorVersion='12';
        elif [[ $releaseVersion =~ ^15.* ]]; then
           majorVersion='15';
        fi;
        ;;

     *"Oracle"* | *"EnterpriseEnterpriseServer"*)
        platform='Oracle_OL'; runningPlatform=$platform;
        if [[ $releaseVersion =~ ^5.* ]]; then
           majorVersion='5'
        elif [[ $releaseVersion =~ ^6.* ]]; then
           majorVersion='6';
        elif [[ $releaseVersion =~ ^7.* ]]; then
           majorVersion='7';
        elif [[ $releaseVersion =~ ^8.* ]]; then
           majorVersion='8';
        fi;
        ;;

     *"CentOS"*)
        platform='RedHat_EL'; runningPlatform='CentOS_';
        if [[ $releaseVersion =~ ^5.* ]]; then
           majorVersion='5';
        elif [[ $releaseVersion =~ ^6.* ]]; then
           majorVersion='6';
        elif [[ $releaseVersion =~ ^7.* ]]; then
           majorVersion='7';
        fi;
        ;;

     *"CloudLinux"*)
        platform='CloudLinux_'; runningPlatform=$platform;
        if [[ $releaseVersion =~ ^6.* ]]; then
           majorVersion='6';
        elif [[ $releaseVersion =~ ^7.* ]]; then
           majorVersion='7';
        fi;
        ;;

     *"Amazon"*)
        platform='amzn'; runningPlatform=$platform;
        if [[ $(uname -r) == *"amzn2"* ]]; then
           majorVersion='2';
        elif [[ $(uname -r) == *"amzn1"* ]]; then
           majorVersion='1';
        fi;
        ;;

     *"RedHat"* | *"Red Hat"*)
        platform='RedHat_EL'; runningPlatform=$platform;
        if [[ $releaseVersion =~ ^5.* ]]; then
           majorVersion='5';
        elif [[ $releaseVersion =~ ^6.* ]]; then
           majorVersion='6';
        elif [[ $releaseVersion =~ ^7.* ]]; then
           majorVersion='7';
        elif [[ $releaseVersion =~ ^8.* ]]; then
           majorVersion='8';
        fi;
        ;;

  esac
}
clear
platform_detect
PlatformL="${platform}${majorVersion}";


echo "Platform is $PlatformL"
echo "Installing/Updating curl, netcat, zip, unzip and lsof..."
if [[ $PlatformL == *"RedHat"* ]]; then
	sudo yum install curl nc lsof -y -q > /dev/null
	sudo yum install zip unzip -y -q > /dev/null

elif [[ $PlatformL == *"Ubuntu"* ]]; then
	sudo apt-get install curl netcat lsof -y -qq > /dev/null
	sudo apt-get install zip unzip -y -qq > /dev/null

elif [[ $PlatformL == *"SuSE"* ]]; then
	sudo zypper install -y curl netcat-openbsd lsof > /dev/null
	sudo zypper install -y zip unzip > /dev/null

elif [[ $PlatformL == *"Oracle"* ]]; then
	sudo yum install curl nc lsof -y -q > /dev/null
	sudo yum install zip unzip -y -q > /dev/null

elif [[ $PlatformL == *"CloudLinux"* ]]; then
	sudo yum install curl nc lsof -y -q > /dev/null
	sudo yum install zip unzip -y -q > /dev/null

elif [[ $PlatformL == *"amzn"* ]]; then
	sudo yum install curl nc lsof -y -q > /dev/null
	sudo yum install zip unzip -y -q > /dev/null

elif [[ $PlatformL == *"Debian"* ]]; then
	sudo apt-get install curl netcat lsof -y -qq > /dev/null
	sudo apt-get install zip unzip -y -qq > /dev/null
fi
echo -e "Installation/Update complete.\n"

# Pre-Variables

# DSaaS URLs
MainURLs=("app.deepsecurity.trendmicro.com" "agents.deepsecurity.trendmicro.com" "dsmim.deepsecurity.trendmicro.com" "relay.deepsecurity.trendmicro.com")
APIURLs=("app.deepsecurity.trendmicro.com/webservice/Manager?WSDL" "app.deepsecurity.trendmicro.com/api" "app.deepsecurity.trendmicro.com/rest")
DCURLs=("files.trendmicro.com")
SPN=("dsaas1100-en-census.trendmicro.com" "deepsecaas11-en.gfrbridge.trendmicro.com" "dsaas.icrc.trendmicro.com" "dsaas-en-f.trx.trendmicro.com" "dsaas-en-b.trx.trendmicro.com" "dsaas.url.trendmicro.com")
UpdateURLs=("iaus.activeupdate.trendmicro.com" "iaus.trendmicro.com" "ipv6-iaus.trendmicro.com" "ipv6-iaus.activeupdate.trendmicro.com")

#XDR URLs
xdrURLs=("ak5ih4ev105f2-ats.iot.us-east-1.amazonaws.com" "azrb5zzyvrkw6-ats.iot.us-east-1.amazonaws.com")

#Functions

ShowRetryMenu (){
echo -e "\n"
echo "Retry? y\n"

}

ShowExportMenu (){
echo -e "\n"
echo "Export to File? y\n"

}



DSaaSChecker (){
            
            echo -e "Checking C1WS Main URLs..." >> /tmp/DSaaS_Pre-check/connection.txt
            echo -e "\n" >> /tmp/DSaaS_Pre-check/connection.txt
			for DSaaSURL in "${MainURLs[@]}"
            do
                DSaaSlist=$(nc -z -v -w 2 $DSaaSURL $DSaaSPort &> /dev/null && echo "Online" || echo "Offline")
                if [[ $DSaaSlist == "Online" ]]; then
                        echo -e "Successfully connected to $DSaaSURL via TCP port $DSaaSPort" >> /tmp/DSaaS_Pre-check/connection.txt
                else
                        echo -e "Failed to connect to $DSaaSURL via TCP port $DSaaSPort" >> /tmp/DSaaS_Pre-check/connection.txt
                fi
            done

            echo -e "\n" >> /tmp/DSaaS_Pre-check/connection.txt
            echo -e "Checking C1WS Download Center URLs..." >> /tmp/DSaaS_Pre-check/connection.txt
            echo -e "\n" >> /tmp/DSaaS_Pre-check/connection.txt
            for DSaaSURL in "${DCURLs[@]}"
			do
				DSaaSlist=$(nc -z -v -w 2 $DSaaSURL $DSaaSPort &> /dev/null && echo "Online" || echo "Offline")
				if [[ $DSaaSlist == "Online" ]]; then
				        echo -e "Successfully connected to $DSaaSURL via TCP port $DSaaSPort" >> /tmp/DSaaS_Pre-check/connection.txt
				else
				        echo -e "Failed to connect to $DSaaSURL via TCP port $DSaaSPort" >> /tmp/DSaaS_Pre-check/connection.txt
				fi
			done

			for DSaaSURL in "${DCURLs[@]}"
			do
				DSaaSlist=$(nc -z -v -w 2 $DSaaSURL $DSaaSPort80 &> /dev/null && echo "Online" || echo "Offline")
				if [[ $DSaaSlist == "Online" ]]; then
				        echo -e "Successfully connected to $DSaaSURL via TCP port $DSaaSPort80" >> /tmp/DSaaS_Pre-check/connection.txt
				else
				        echo -e "Failed to connect to $DSaaSURL via TCP port $DSaaSPort80" >> /tmp/DSaaS_Pre-check/connection.txt
				fi
			done

            echo -e "\n" >> /tmp/DSaaS_Pre-check/connection.txt     
            echo -e "Checking C1WS Active Update URLs..." >> /tmp/DSaaS_Pre-check/connection.txt
            echo -e "\n" >> /tmp/DSaaS_Pre-check/connection.txt
            for DSaaSURL in "${UpdateURLs[@]}"
            do
                DSaaSlist=$(nc -z -v -w 2 $DSaaSURL $DSaaSPort &> /dev/null && echo "Online" || echo "Offline")
                if [[ $DSaaSlist == "Online" ]]; then
                        echo -e "Successfully connected to $DSaaSURL via TCP port $DSaaSPort" >> /tmp/DSaaS_Pre-check/connection.txt
                else
                        echo -e "Failed to connect to $DSaaSURL via TCP port $DSaaSPort" >> /tmp/DSaaS_Pre-check/connection.txt
                fi
            done

            for DSaaSURL in "${UpdateURLs[@]}"
            do
                DSaaSlist=$(nc -z -v -w 2 $DSaaSURL $DSaaSPort80 &> /dev/null && echo "Online" || echo "Offline")
                if [[ $DSaaSlist == "Online" ]]; then
                        echo -e "Successfully connected to $DSaaSURL via TCP port $DSaaSPort80" >> /tmp/DSaaS_Pre-check/connection.txt
                else
                        echo -e "Failed to connect to $DSaaSURL via TCP port $DSaaSPort80" >> /tmp/DSaaS_Pre-check/connection.txt
                fi
            done

            echo -e "\n" >> /tmp/DSaaS_Pre-check/connection.txt		
            echo -e "Checking C1WS Smart Protection Network URLs..." >> /tmp/DSaaS_Pre-check/connection.txt
            echo -e "\n" >> /tmp/DSaaS_Pre-check/connection.txt
            for DSaaSURL in "${SPN[@]}"
			do
				DSaaSlist=$(nc -z -v -w 2 $DSaaSURL $DSaaSPort &> /dev/null && echo "Online" || echo "Offline")
				if [[ $DSaaSlist == "Online" ]]; then
				        echo -e "Successfully connected to $DSaaSURL via TCP port $DSaaSPort" >> /tmp/DSaaS_Pre-check/connection.txt
				else
				        echo -e "Failed to connect to $DSaaSURL via TCP port $DSaaSPort" >> /tmp/DSaaS_Pre-check/connection.txt
				fi
			done

			for DSaaSURL in "${SPN[@]}"
			do
				DSaaSlist=$(nc -z -v -w 2 $DSaaSURL $DSaaSPort80 &> /dev/null && echo "Online" || echo "Offline")
				if [[ $DSaaSlist == "Online" ]]; then
				        echo -e "Successfully connected to $DSaaSURL via TCP port $DSaaSPort80" >> /tmp/DSaaS_Pre-check/connection.txt
				else
				        echo -e "Failed to connect to $DSaaSURL via TCP port $DSaaSPort80" >> /tmp/DSaaS_Pre-check/connection.txt
				fi
			done

            echo -e "\n" >> /tmp/DSaaS_Pre-check/connection.txt
            echo -e "Checking C1WS XDR URLs..." >> /tmp/DSaaS_Pre-check/connection.txt
            echo -e "\n" >> /tmp/DSaaS_Pre-check/connection.txt
            for DSaaSURL in "${xdrURLs[@]}"
            do
                DSaaSlist=$(nc -z -v -w 2 $DSaaSURL $DSaaSPort &> /dev/null && echo "Online" || echo "Offline")
                if [[ $DSaaSlist == "Online" ]]; then
                        echo -e "Successfully connected to $DSaaSURL via TCP port $DSaaSPort" >> /tmp/DSaaS_Pre-check/connection.txt
                else
                        echo -e "Failed to connect to $DSaaSURL via TCP port $DSaaSPort" >> /tmp/DSaaS_Pre-check/connection.txt
                fi
            done		
}



#Main Program

until [[ $input == 'n' ]]
do
			#Variables
            sudo rm -rf /tmp/DSaaS_Pre-check/
			sudo mkdir /tmp/DSaaS_Pre-check/
			DSaaSPort80=80
			DSaaSPort=443


			#Check TCP connection to DSaaS
			echo "Checking connection to the URLs of Cloud One Workload Security..."
			DSaaSChecker
            echo "Done!"
            sleep 2
            echo "Displaying Results..."
            sleep 5
            echo -e "\n\n"
            cat /tmp/DSaaS_Pre-check/connection.txt
            echo -e "\n\n"

    ShowRetryMenu
	read input
done

ShowExportMenu
read input

case $input in
    y)
        echo "Results.txt saved on current directory!"
        sudo cp /tmp/DSaaS_Pre-check/connection.txt ./results.txt
        sudo rm -rf /tmp/DSaaS_Pre-check/
        exported=1
    ;;
    Y)
        echo "Results.txt saved on current directory!"
        sudo cp /tmp/DSaaS_Pre-check/connection.txt ./results.txt
        sudo rm -rf /tmp/DSaaS_Pre-check/
        exported=1
    ;;
    n)
        echo "Results Not Saved!"
        sudo rm -rf /tmp/DSaaS_Pre-check/
        exported=0
    ;;
    N)
        echo "Results Not Saved!"
        sudo rm -rf /tmp/DSaaS_Pre-check/
        exported=0
    ;;
esac
echo "Thank you for using the tool!"