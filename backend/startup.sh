#!/bin/bash
# It's assumed that this script will be run from its directory!

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 OneOnOne/manage.py makemigrations 
python3 OneOnOne/manage.py migrate

python3 OneOnOne/manage.py makemigrations calendars
python3 OneOnOne/manage.py migrate calendars

python3 OneOnOne/manage.py makemigrations contacts
python3 OneOnOne/manage.py migrate contacts