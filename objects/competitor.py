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
    
    CalculatedLivePos = str()
    CalculatedTimeGap = float()
    
    def __init__(self, compNum):
        self.number = compNum

    def __repr__(self) -> str:
        return "id:"+str(self.number)+", gps:"+str(self.lastknownGPS)+", lap:"+str(self.lastKnownLap)+", pos:"+str(self.lastKnownPos)+", speed:"+str(self.lastKnownSpeed)
