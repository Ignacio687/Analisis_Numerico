#!bin/bash

pip install env
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
python3 app.py