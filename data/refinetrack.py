# This file reads a json file and iterates over the ['points'] array, 
# between each two points, it append another point that is in the middle of the two points. (center of the line between the two points)
# Then, it saves the new more refiened version of the track in a new json file.

import json

with open("refinedTrack3.json", "r") as f:
    data = json.load(f)['points']
    
    newData = []
    for i in range(len(data)-1):
        newData.append(data[i])
        newData.append([(data[i][0]+data[i+1][0])/2, (data[i][1]+data[i+1][1])/2])
    newData.append(data[-1])
    with open("refinedTrack4.json", "w") as f:
        json.dump({"trackname": "refinedTrack", "points": newData}, f)


