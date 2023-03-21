import json
import time
import threading
import requests
"""
THIS FILE IS FOR DEVELOPMENT PURPOSE ONLY. IT IS USED TO EASILY FAKE CONNECTION TO SERVER AND SEND FAKE GPS DATA
"""
with open("data/gps.json", "r") as f:
    data = json.load(f)['points']

COMPETITORS = 3
LAPS = 1
url = "http://localhost:8000/"


class fakeCompetitor(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay
        self.laptimes = []

    def run(self):
        for j in range(LAPS):
            startLap = time.time()
            for i in data:
                time.sleep(self.delay)
                dict = {"id":self.name,"latitude":i['x'],"longitude":i['y'],"speed":30,"gForce":1.01}
                x = requests.post(url, json = dict)
                # print(x.text)
            self.laptimes.append(time.time()-startLap)
        print(self.name, "finished in ", sum(self.laptimes))

ids = [88888]
delays = [0.25]
newThread = fakeCompetitor(0, ids[0], delays[0])
newThread.start()