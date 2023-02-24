#!/bin/bash
python3 -u gpsModule.py > logs/gpsModLog.log 2>&1 &
python3 -u timingmodule.py https://speedhive.mylaps.com/LiveTiming/CEHQNRVR-2147485181/Active > logs/timingModLog.log 2>&1 &
python3 -u compModule.py > logs/compModLog.log 2>&1 &
python3 -u trackModule.py > logs/trackModLog.log 2>&1 &
