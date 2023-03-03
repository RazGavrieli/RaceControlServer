#!/bin/bash
python3.10 -u gpsModule.py > logs/gpsModLog.log 2>&1 &
python3.10 -u timingmodule.py $1 > logs/timingModLog.log 2>&1 & 
# python3.10 -u SuggestionsGenerator.py > logs/suggestionsModLog.log 2>&1 &
