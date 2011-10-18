#!/bin/bash
export PYTHONPATH=$PYTHONPATH:`pwd`
export DJANGO_SETTINGS_MODULE=planetex.settings
python2.3 update.py