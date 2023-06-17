from compModule import compMod
from trackModule import trackMod

import threading 
# import pygame 

# import random 

import requests
import json

#import sys 
#import os # for cli

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
    # this function raises a suggestion to the server.
    if suggestion not in suggestions:
        suggestions.append(suggestion)

def yellow_flags_detector():
    # this function iterates over all competitors and check if their speed is lower than 10km/h, if so it checks if
    # the compettitor did not move. If so, it creates a yellow flag for the competitor's location.      
    while True:
        time.sleep(0.25)   
        for competitor in comps.competitors.keys():
            if comps.get_competitor(competitor).lastKnownSpeed < YELLOW_FLAGS_SPEED:
                suggestion = "competitor "+str(competitor)+" is slow at "+str(comps.get_competitor(competitor).lastknownGPS)
                suggestion_raise(suggestion)
                if comps.get_competitor(competitor).CalculatedLocation not in yellows:
                    yellows.append(comps.get_competitor(competitor).CalculatedLocation)
                # TODO Raise a suggestion for yellow flag at competitor's location.
            #elif comps.get_competitor(competitor).lastKnownGforce > YELLOW_FLAGS_GFORCE:
            #    suggestion_raise("competitor "+str(competitor)+" is in a crash at "+str(comps.get_competitor(competitor).lastknownGPS))
            #    # TODO Raise a suggestion for yellow flag at competitor's location.
            elif comps.get_competitor(competitor).CalculatedLocation in yellows:
                yellows.remove(comps.get_competitor(competitor).CalculatedLocation)
            
def live_position_calculator():
    # this function calculates the live position of each competitor and updates the competitor's the 
    # competitor's CalculatedLivePos attribute.
    # The calculation is a sort function, sorting the competitors by their last known lap(lastKnownLap) AND their last known position(CalculatedLocation).
    while True:
        time.sleep(0.25)    
        listOfCompetitors = []
        for competitor in comps.competitors.keys():
            listOfCompetitors.append(comps.get_competitor(competitor))
        listOfCompetitors.sort(key=lambda x: (x.lastKnownLap, x.CalculatedLocation), reverse=True)
        for index in range(len(listOfCompetitors)):
            comps.competitors[listOfCompetitors[index].number].CalculatedLivePos = index + 1
            
def location_calculator():
    """This function calculates the location of each competitor and updates the competitor's the calculatedLocation attribute."""
    while True:
        time.sleep(0.1)
        # this function calculates the location of each competitor and updates the competitor's the calculatedLocation attribute.
        for competitor in comps.competitors.keys():
            location = comps.get_competitor(competitor).lastknownGPS
            if location == () or location is None:
                continue
            # Go over the track's list of checkpoints (track.get_racetrack) and find the closest checkpoint to the competitor's location.
            # Then, calculate the distance between the competitor's location and the checkpoint.
            inPits = False
            closestPoint = track.get_racetrack()[0]
            closestPointIndex = 0
            for index, point in enumerate(track.get_racetrack()):
                if distance(location, point) < distance(location, closestPoint):
                    closestPoint = point
                    closestPointIndex = index

            for point in enumerate(track.get_pits()):
                if distance(location, point) < distance(location, closestPoint) and comps.get_competitor(competitor).lastKnownSpeed < 40:
                    closestPoint = point
                    closestPointIndex = index
                    inPits = True

            if inPits and not comps.get_competitor(competitor).inPits:
                comps.get_competitor(competitor).lastKnownPitEntry = time.time()
            if not inPits and comps.get_competitor(competitor).inPits:
                comps.get_competitor(competitor).lastKnownPitExit = time.time()
                # TODO Raise a suggestion for competitor's pit stop time.
            
            comps.competitors[competitor].lastCalculatedLocation = comps.competitors[competitor].CalculatedLocation
            comps.competitors[competitor].CalculatedLocation = closestPointIndex
            comps.competitors[competitor].inPits = inPits
        
def distance(point1: tuple, point2: tuple):
    # this function calculates the distance between two points.
    return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)**0.5

def live_laps_calculator():
    # this function calculates the live laps of each competitor and updates the 
    # competitor's CalculatedLiveLap attribute.
    # The function checks for differences between the last known lap and the calculated lap, if there is a difference
    # the function should check again after 1 second, if the difference is still there, it should raise a suggestion
    while True:
        time.sleep(0.1)
        for competitor in comps.competitors.keys():
            if comps.get_competitor(competitor).lastCalculatedLocation > len(track.get_racetrack())-CLOSE_TO_SF_LINE_DIST_IN_UNITS:
                if comps.get_competitor(competitor).lastCalculatedLocation > comps.get_competitor(competitor).CalculatedLocation:
                    comps.get_competitor(competitor).CalculatedLiveLaps += 1
                    if comps.get_competitor(competitor).CalculatedLiveLaps != comps.get_competitor(competitor).lastKnownLap:
                        #print("Competitor ", competitor, " is in lap ", comps.get_competitor(competitor).CalculatedLiveLaps, " but last known lap is ", comps.get_competitor(competitor).lastKnownLap)
                        suggestion_raise("competitor "+str(competitor)+ " is in lap "+str(comps.get_competitor(competitor).CalculatedLiveLaps)+" but last known lap is "+str(comps.get_competitor(competitor).lastKnownLap))
                        # TODO Raise a suggestion for fixing the competitor's last known lap.

def blue_flags_detector():
    # This functions checks if a leadingCompetitor laps another traficCompetitor.
    # If so, it raises a suggestion for blue flags.
    while True:
        time.sleep(0.25)
        for leadingCompetitor in comps.competitors.keys():
            for trafficCompetitor in comps.competitors.keys():
                if leadingCompetitor != trafficCompetitor:
                    if (comps.get_competitor(leadingCompetitor).lastKnownPos < comps.get_competitor(trafficCompetitor).lastKnownPos and # if leading is actually leading
                        comps.get_competitor(leadingCompetitor).lastKnownLap > comps.get_competitor(trafficCompetitor).lastKnownLap and # if leading's lap is bigger than traffic's lap (but not equals! - important)
                        (- BLUE_FLAGS_DIST_IN_UNITS < comps.get_competitor(leadingCompetitor).CalculatedLocation - comps.get_competitor(trafficCompetitor).CalculatedLocation < 0 or 
                        comps.get_competitor(leadingCompetitor).CalculatedLocation >= len(track.get_racetrack()) - BLUE_FLAGS_DIST_IN_UNITS and comps.get_competitor(trafficCompetitor).CalculatedLocation <= BLUE_FLAGS_DIST_IN_UNITS)): # if traffic's location on track is actually physically infront of leading's location on track
                        #print("Competitor ", trafficCompetitor, " is in ", leadingCompetitor," way!")
                        suggestion_raise("competitor "+str(trafficCompetitor)+ "("+str(comps.get_competitor(trafficCompetitor).lastKnownLap)+") is in "+str(leadingCompetitor)+"("+str(comps.get_competitor(leadingCompetitor).lastKnownLap)+") way!")
                        if (leadingCompetitor, trafficCompetitor) not in blues:
                            blues.append((leadingCompetitor, trafficCompetitor))
                        # TODO Raise a suggestion for blue flag at traffic competitor's location.
                    elif (leadingCompetitor, trafficCompetitor) in blues: # No need for blue flags bettween these two competitors.
                        blues.remove((leadingCompetitor, trafficCompetitor))

def pits_monitor():
    """for every competitor, check if he is in the pits. If so, check his speed. If his speed is above PITS_LEGAL_SPEED, raise a suggestion for pit speed violation."""
    while True:
        time.sleep(0.25)
        for competitor in comps.competitors.keys():
            if comps.get_competitor(competitor).inPits and comps.get_competitor(competitor).lastKnownSpeed > PITS_LEGAL_SPEED:
                #print("Competitor ", competitor, " is in the pits but his speed is ", comps.get_competitor(competitor).lastKnownSpeed)
                suggestion_raise("competitor "+str(competitor)+" is speeding in pits ("+str(comps.get_competitor(competitor).lastKnownSpeed)+")")
                # TODO Raise a suggestion for pit speed violation.

def print_results():
    """
    This function prints the results of the calculations, used for debugging purposes
    """
    while True:
        time.sleep(0.25)
        print("------§§§------ ResultS ------§§§------")
        #os.system('cls' if os.name == 'nt' else 'clear')
        for compk in comps.competitors.keys():
            comp = comps.get_competitor(str(compk))
            print("NUM:", comp.number, "POS:", comp.lastKnownPos, "LIVEPOS:", comp.CalculatedLivePos, "LAP:", comp.lastKnownLap, "LIVELAP:", comp.CalculatedLiveLaps, "CAL_LOC:", comp.CalculatedLocation)
        for suggestion in suggestions:
            print(suggestion)
        #print(track.RaceTrack)


def send_line(id, a, b, flag):
    http_url = 'http://webapp:3001/api/track'
    headers = {'Content-type': 'application/json'}
    try:
        requests.post(http_url, data=json.dumps({'id': id, 'a': a, 'b': b, 'flag': flag}), headers=headers, stream=True)
    except Exception as e:
        print(e)

def send_point(id, x, y):
    http_url = 'http://webapp:3001/api/competitors'
    headers = {'Content-type': 'application/json'}
    try:    
        requests.post(http_url, data=json.dumps({'id': id, 'x': x, 'y': y}), headers=headers, stream=True)
    except Exception as e:
        print(e)

def draw_track():
   # Initialize pygame and create a screen
    # pygame.init()
    # screen = pygame.display.set_mode((800, 600))

    # # Set the background color.
    # bg_color = (230, 230, 230)
    # screen.fill(bg_color)

    def normalize_point(point: tuple):
        """This function gets a point in which x is in range [ 35.1, 35.29 ], and y is in range [ 31.1, 31.29 ]
        The problem is that the points are in a very small range, so the screen is too small to fit the points.
        So this function returns a tuple of points in range [0, 800] and [0, 600], and the points will be scattered on this screen to fit the entire screen
        To do that, we need to find the maximum and minimum values of x and y, and then we need to normalize the points to fit the screen."""
        # Find the maximum and minimum values of x and y
        max_x = 0
        min_x = 1000
        max_y = 0
        min_y = 1000
        for i in range(len(track.get_racetrack())):
            if track.get_racetrack()[i] == (0, 0):
                return (0, 0)
            if track.get_racetrack()[i][0] > max_x:
                max_x = track.get_racetrack()[i][0]
            if track.get_racetrack()[i][0] < min_x:
                min_x = track.get_racetrack()[i][0]
            if track.get_racetrack()[i][1] > max_y:
                max_y = track.get_racetrack()[i][1]
            if track.get_racetrack()[i][1] < min_y:
                min_y = track.get_racetrack()[i][1]
        # Normalize the points
        if max_x-min_x == 0 or max_y-min_y == 0:
            return (0, 0)
        x = int((point[0]-min_x)*(800/(max_x-min_x)))
        y = int((point[1]-min_y)*(600/(max_y-min_y)))

        
        #print(x, y)
        return (-x+800, y)

    while True:
        # for event in pygame.event.get():
        #     # if the user clicks the close button, exit the program
        #     if event.type == pygame.QUIT:
        #         sys.exit()
        #     # else if SIGINT is received, exit the program
        #     elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        #         sys.exit()
        #     # else if the process is killed using the bash command 'pkill', exit the program
        #     elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        #         sys.exit()


        # # Update the Pygame display
        # pygame.display.update()

        # # Fill the screen with a gray background color
        # screen.fill((128, 128, 128))
        # # Draw the track
        for i in range(len(track.get_racetrack())):
            if i == len(track.get_racetrack())-1:
                # pygame.draw.line(screen, (60, 0, 0), normalize_point(track.get_racetrack()[i]), normalize_point(track.get_racetrack()[0]), 2)
                send_line(i, normalize_point(track.get_racetrack()[i]), normalize_point(track.get_racetrack()[0]), 0)
            else:
                # pygame.draw.line(screen, (170, 0, 0), normalize_point(track.get_racetrack()[i]), normalize_point(track.get_racetrack()[i+1]), 2)
                send_line(i, normalize_point(track.get_racetrack()[i]), normalize_point(track.get_racetrack()[i+1]), 0)

        for leadingComp, trafficComp in blues:
            for checkpoint in range(comps.get_competitor(leadingComp).CalculatedLocation, comps.get_competitor(trafficComp).CalculatedLocation):  
                send_line(checkpoint, normalize_point(track.get_racetrack()[checkpoint]), normalize_point(track.get_racetrack()[checkpoint+1]), 1)

        for i in yellows:
            send_line(i, normalize_point(track.get_racetrack()[i]), normalize_point(track.get_racetrack()[(i+1)%len(track.get_racetrack())]), 2)
        # Draw the competitors
        for compk in comps.competitors.keys():
            comp = comps.get_competitor(str(compk))
            if len(comp.lastknownGPS) == 2:
                # draw a circle representing the competitor
                # pygame.draw.circle(screen, comp.color, normalize_point(comp.lastknownGPS), 5)
                send_point(compk, *normalize_point(comp.lastknownGPS))
                # write the competitor's number inside the circle
                # font = pygame.font.SysFont('Arial', 20)
                # text = font.render(str(compk), True, (0, 0, 0))
                # screen.blit(text, normalize_point(comp.lastknownGPS))


        # Make the most recently drawn screen visible.
        # pygame.display.flip()


def publish_calculations():
    http_url = 'http://webapp:3001/api/msgs'
    sents = []
    message = ''
    while True:
        time.sleep(0.25)
        flag = False
        for i in suggestions:
            if i not in sents:
                sents.append(i)
                headers = {'Content-type': 'application/json'}
                try:
                    requests.post(http_url, data=json.dumps({'content': i}), headers=headers, stream=True)
                except Exception as e:
                    print(e)



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
    #print_results_thread = threading.Thread(target=print_results)
    publish_calculations_thread = threading.Thread(target=publish_calculations)

    yellow_flags_thread.start()
    blue_flags_thread.start()
    location_calculator_thread.start()
    live_position_calculator_thread.start()
    live_laps_calculator_thread.start()
    pits_monitor_thread.start()
    #print_results_thread.start()
    publish_calculations_thread.start()

    #publish_calculations_thread.join()
    draw_track() # pygame
 