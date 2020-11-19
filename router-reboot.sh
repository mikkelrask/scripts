#!/bin/sh

# Simple script pinging 8.8.8.8 (Google DNS) to check if we get any repsonse
# If not, we'll wait for 30 seconds, and give it another go. 
# If still no luck, it'll reboot the router.
# I put `*/15 * * * * /router-reboot.sh` in my crontab to run 
# the script every 15 minutes and if theres any problem it will
# append the timestamp in reboot.log i the same directory as the script location
# To edit your crontab you go `crontab -e`
# 
# This is running directly on my router flashed with OpenWRT/LEDE (openwrt.org) 


if ping -c 1 8.8.8.8 &> /dev/null
then 
	exit	
else
	sleep 30
	if ping -c 1 8.8.8.8 &> /dev/null
	then 
		exit
	else
		date >> reboot.log
		reboot
	fi
fi
