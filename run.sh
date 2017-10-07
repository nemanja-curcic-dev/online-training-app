#!/bin/bash
#
# Script for starting virtual environment and development server
#
# Created by Nemanja Curcic

# Global declarations
location="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/env"


# activate virtual enviroment
source env/bin/activate
printf "Started virtual enviroment at $location\n"
sleep 1

# runserver
if [ $# -eq 0 ]
then
    python manage.py runserver
else
   python manage.py runserver -p $1
fi
