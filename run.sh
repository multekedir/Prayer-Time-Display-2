#!/bin/bash

clear
export SETTINGS=./dev.settings
python3.7 -m flask run
firefox -url http://127.0.0.1:5000/ & xdotool search --sync --onlyvisible --class "Firefox" windowactivate key F11
