# import networkx as nx

class track:
    """
    this class holds all the information about the racetrack. 

    Attributes:
        trackList (list): A list of GPS points that represent the track's layout by order. The first point should be the S/F line.
        sectorsList (list): A list of GPS points that define the start of each sector by order. The first point should be the S/F line.
        pitsList (list): A list of GPS points that define the pit lane by order. The first point is the pit entry and the last point is the pit exit.
        marshelList (list): A list of GPS points that represent the location of each marshal post on the racetrack.

    Methods:
        __init__(): Initializes a new Track object with the given track information.
        __repr__() -> str: Returns a string representation of the Track object.
    """
    trackList = list()
    sectorsList = list()
    pitsList = list()
    marshelList = list()
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return "track:"+str(self.trackList)+", pits:"+str(self.pitsList)+", sectors:"+str(self.sectorsList)+", marshells:"+str(self.marshelList)
