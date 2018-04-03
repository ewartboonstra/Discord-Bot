#!/bin/bash

if [ "$(whoami)" != "root" ]; then
	echo This command requires root privileges
	exit
fi

echo Installing the pip package manager for python3

apt-get install -y python3-pip
if [ $? -eq 0 ]; then
	# It succeeded
	echo "Succesfully installed python3-pip"
	echo "Installing the discord.py library"
	python3 -m pip install -U discord.py
	if [ $? -eq 0 ]; then
		echo "Succesfully installed discord.py"
	else
		echo "Failed to install discord.py"
	fi
else
	echo "Failed to install python3-pip"
fi

echo "Script is done executing"
exit
