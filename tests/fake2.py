import json
import time
import threading
import requests
import random
import pika
import os # for cli

LAPS = 5
COMPETITORS = 4
comps = []
timeDelay = 0.25


class fakeCompetitor(threading.Thread):
    def __init__(self, name, howfast):
        threading.Thread.__init__(self)
        self.howFast = howfast
        self.name = name
        self.checkpointsPassed = 0
        self.lap = 0

        self.currLapTime = time.time()
        self.lastLapTime = 0
        

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', socket_timeout=None))
        channel = connection.channel()
        channel.queue_declare(queue='TIMING')

        for j in range(LAPS):
            # goes through start\finish line
            self.lap = j+1
            currPos = comps.index(self)+1 # this is used for asserting the position of the competitor
            compDict = {'id': self.name, 'laps': self.lap, 'pos': currPos}
            channel.basic_publish(exchange='', routing_key='TIMING', body=str(compDict), properties=pika.BasicProperties(headers={"queue_name": "TIMING", "additional_property": "value"}))
            self.lastLapTime = time.time() - self.currLapTime
            self.currLapTime = time.time()
            for index, i in enumerate(data):
                self.checkpointsPassed += 1

                if index % self.howFast != 0:
                    continue
                
                time.sleep(timeDelay)
                dict = {"id":self.name,"latitude":i[0]+(random.randint(-5, 5)/10000000),"longitude":i[1]+(random.randint(-5, 5)/10000000),"speed":30,"gForce":1.01}
                try:
                    requests.post(url, json = dict)
                except Exception as e:
                    print(f"Error: {e}. Retrying...")
                # print(x.text)

"""
THIS FILE IS FOR DEVELOPMENT PURPOSE ONLY. IT IS USED TO EASILY FAKE CONNECTION TO SERVER AND SEND FAKE GPS DATA
"""
with open("data/refinedTrack2.json", "r") as f:
    data = json.load(f)['points']

url = "http://localhost:8000/"
for index, i in enumerate(data):
    if index%5!=0:
        continue
    time.sleep(0.05)
    dict = {"id":88888,"latitude":i[0],"longitude":i[1],"speed":15,"gForce":1.01}
    x = requests.post(url, json = dict)


trackLength = len(data)
print("track sent")
time.sleep(1)
print("green flag")

for i in range(COMPETITORS):
    comps.append(fakeCompetitor(70+i, 3+min(i, 5)))

for i in comps:
    i.start()

while True:
    time.sleep(timeDelay)
    timeDelay = 0.25
    os.system('cls' if os.name == 'nt' else 'clear')
    comps = sorted(comps, key=lambda x: x.checkpointsPassed, reverse=True)
    for index, i in enumerate(comps):
        print(f"{index+1}. {i.name} - {i.checkpointsPassed} - {i.checkpointsPassed%trackLength} - {i.lap} - {i.lastLapTime} - {time.time() - i.currLapTime}")

    for leadingComp in comps:
        for trafficComp in comps:
            if leadingComp.name != trafficComp.name:
                if leadingComp.lap > trafficComp.lap and -15 < leadingComp.checkpointsPassed%trackLength - trafficComp.checkpointsPassed%trackLength < 0:
                    print(f"{leadingComp.name} is being held up by {trafficComp.name}")
                    timeDelay = 0.25
                else:
                    break