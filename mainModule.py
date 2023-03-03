from compModule import compMod
from trackModule import trackMod
import time 

import threading 
import pygame 

import random 

import sys 
import os # for cli

import time



BLUE_FLAGS_DIST_IN_UNITS = 15
CLOSE_TO_SF_LINE_DIST_IN_UNITS = 15
YELLOW_FLAGS_SPEED = 10
YELLOW_FLAGS_GFORCE = 4
PITS_LEGAL_SPEED = 30
suggestions = []
blues = []
yellows = []
def suggestion_raise(suggestion):
    pass

def yellow_flags_detector():
    pass    
            
def live_position_calculator():
    pass 
            

def location_calculator():
    pass 

def distance(point1: tuple, point2: tuple):
    # this function calculates the distance between two points.
    return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)**0.5

def live_laps_calculator():
    pass 

def blue_flags_detector():
    pass 

def pits_monitor():
    pass 

def print_results():
    pass 

def draw_track():
    pass

    
if __name__ == "__main__":
    comps = compMod()
    track = trackMod()
    comps.start()
    track.start()


    yellow_flags_thread = threading.Thread(target=yellow_flags_detector)
    blue_flags_thread = threading.Thread(target=blue_flags_detector)
    location_calculator_thread = threading.Thread(target=location_calculator)
    live_position_calculator_thread = threading.Thread(target=live_position_calculator)
    live_laps_calculator_thread = threading.Thread(target=live_laps_calculator)
    pits_monitor_thread = threading.Thread(target=pits_monitor)
    print_results_thread = threading.Thread(target=print_results)

    yellow_flags_thread.start()
    blue_flags_thread.start()
    location_calculator_thread.start()
    live_position_calculator_thread.start()
    live_laps_calculator_thread.start()
    pits_monitor_thread.start()
    print_results_thread.start()

    