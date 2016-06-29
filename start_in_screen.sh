#!/bin/bash

name_of_screen="auriga"

if screen -S $name_of_screen -X select .; then
	echo "a screen session was found"
else
	echo "a screen session was not found; making one now"
	screen -Udm -S $name_of_screen
fi

screen -S $name_of_screen -X stuff $'./gunicorn_server_start\n'
