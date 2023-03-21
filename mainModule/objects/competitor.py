import random

class competitor:
    """
    Represents a competitor in a race.

    Attributes:
        number (int): The competitor's race number.
        lastKnownPos (int): The competitor's last known position in the race.
        lastKnownLap (int): The competitor's last known lap in the race.
        lastknownGPS (tuple): The competitor's last known GPS coordinates.
        lastKnownSpeed (float): The competitor's last known speed.
        CalculatedLivePos (str): The competitor's calculated live position in the race.
        CalculatedTimeGap (float): The competitor's calculated time gap from the leader.

    Methods:
        __init__(self, compNum: int): Initializes a new Competitor object with the given race number.
        __repr__(self) -> str: Returns a string representation of the Competitor object.
    """
    lastKnownPos = int()
    lastKnownLap = int()
    
    lastknownGPS = tuple()
    lastKnownSpeed = float()
    lastKnownGforce = float()

    lastKnownPitEntry = float()
    lastKnownPitExit = float()

    CalculatedLocation = int()
    lastCalculatedLocation = int()
    CalculatedLivePos = str()
    CalculatedLiveLaps = 1
    CalculatedTimeGap = float()
    inPits = bool()
    
    def __init__(self, compNum):
        self.number = compNum
        self.inPits = False
        self.color = (random.randint(0,244),random.randint(0,244),random.randint(0,244))

    def __repr__(self) -> str:
        if len(self.lastknownGPS) != 2:
            self.lastknownGPS = (0,0)
        # return "id:"+str(self.number)+", gps:("+str("{:.2f}".format(self.lastknownGPS[0]))+","+str("{:.2f}".format(self.lastknownGPS[1]))+"), lap:"+str(self.lastKnownLap)+", pos:"+str(self.lastKnownPos)+", calpos:"+str(self.CalculatedLivePos)+", calloc:"+str(self.CalculatedLocation)+", speed:"+str(self.lastKnownSpeed)+", timegap:"+str(self.CalculatedTimeGap)
        return "id:"+str(self.number)+", lap:"+str(self.lastKnownLap)+"callap:"+str(self.CalculatedLiveLaps)+", pos:"+str(self.lastKnownPos)+", calpos:"+str(self.CalculatedLivePos)+", calloc:"+str(self.CalculatedLocation)