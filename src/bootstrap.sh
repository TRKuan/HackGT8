#!/bin/sh
export FLASK_ENV=development
export FLASK_APP=./index.py
flask run -h 0.0.0.0
