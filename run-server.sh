#!/bin/bash

gnome-terminal -e "python3 API/API.py"
gnome-terminal -e "http-server AdminApp/app"

cd AdminApp/app
gnome-terminal -e "sudo grunt watch"
