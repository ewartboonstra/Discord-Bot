#!/bin/bash

if [ "$(whoami)" != "root" ]; then
	# We need root privileges in order to execute the reboot command
	echo This command requires root privileges, otherwise the reboot command might fail
fi

echo "Downloading new script..."
wget --output-document=new_script.py https://raw.githubusercontent.com/ewartboonstra/Discord-Bot/master/bot/__main__.py
echo "Update script downloaded"
hashf1="md5 new_script.py"
hashf2="md5 jackbot_main.py"
if [ ! "$hashf1" = "$hashf2" ]; then
	# If new script was found, make a backup of the old script
	mv -f jackbot_main.py jackbot_main.py.bak
fi
mv -f new_script.py jackbot_main.py
echo "Script is updated"

file="/boot/reboot_pi_on_exit"

function rebootOrExit
{
	# If /boot/reboot_pi_on_exit file exist, we (attempt) to reboot the pi on exit
	if [ -f "$file" ]; then
		reboot
	fi
}

until python3 jackbot_main.py; do
	echo "Discord bot crashed with exit code $?. Respawning.." >&2
	sleep 1
	rebootOrExit
done
