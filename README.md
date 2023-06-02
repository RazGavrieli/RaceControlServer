# RaceControlServer
<img align="left" width="210" alt="image" src="https://github.com/RazGavrieli/RaceControlServer/assets/90526270/6d2fb701-79f4-4a7c-8414-9461f091d867"> 

# RACE CONTROL: Next-Gen Race Management System
Welcome to RACE CONTROL, a project aimed at revolutionizing car race management. We believe that technology can play a significant role in enhancing and simplifying the tasks associated with managing a car race. This project seeks to transform the racing experience for race track staff and marshals, bringing efficiency, accuracy, and precision to their fingertips.

<img align="right" width="210" alt="image" src="https://github.com/RazGavrieli/RaceControlServer/assets/90526270/4131bbf7-73f3-448c-bc86-e02f273939d4">

RACE CONTROL is a data-driven solution that brings together a variety of sensors and a server that interacts seamlessly with the existing timing system on the race track. The goal is to gather, process, and present a clear and comprehensive view of what's happening on the racetrack in real-time.

The primary components of RACE CONTROL include an Android app (for sensor data transmission), a data-receiving server, a set of algorithms for real-time data analysis, and a user-friendly graphical user interface (GUI) for the race director.

This system, by presenting key data like competitor positions, potential flag requirements, and pit stop occurrences, empowers the race director to make immediate and informed decisions, ensuring a safer and well-managed racing event.

Please note: This project focuses on enhancing the experience for the race track staff and marshals, and not for the drivers or viewers. Additionally, RACE CONTROL is designed to integrate into a competitive environment without disrupting existing timing systems and procedures.

# System Architecture 
## High-level system view
In our design, each method of data collection from the racetrack is encapsulated in an individual module. This approach promotes future extensibility as we can easily add new modules to incorporate advanced data collection methods. The following diagram illustrates the highest-level view of these modules, with the modules on the left representing racetrack sensors. More details about the central Main module will follow in the next section.

<p align="center">
<img width="565" alt="image" src="https://github.com/RazGavrieli/RaceControlServer/assets/90526270/eb70f52d-2c63-4e22-ba95-da50f00ce5b4">
</p>

## Main Module
The Main module acts as the heart of our system, being the most complex subsystem. It is composed of various sub-modules, each performing a unique role.

Data streams into the Main module through RabbitMQ, which allows us to easily integrate new sensors and accommodate various types of data in the future.

Upon receiving the data, we utilize two modules to organize and manage track entities: The race track itself, and a list of competitors. The raw data transforms into meaningful information by initializing the relevant entities. Subsequently, the suggestionGenerator code updates this information according to specific calculations. Moreover, various detectors generate suggestions based on the received and processed data.

Below is a diagram illustrating the structure and flow within the Main module:

<p align="center">
  <img src="https://github.com/RazGavrieli/RaceControlServer/assets/90526270/de3a1aaa-83c5-4234-a2f7-b0a862bc2630">
</p>
This modular and dynamic design makes our system flexible, scalable, and ready for future expansions and enhancements.

## Entities
As mentioned above, there are two main entities in the project. In our software solution, those entities are presented as objects:
```python
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
 ```
And the racetrack itself: 
```python
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
```
## Design Rational
You may have noticed that most of the computing is done over the cloud, data is sent from the race-track directly to a cloud server, where it is managed and becomes relevant information. Then the data is being anaylized and decisions are sent back to the race-track over the network. 

The reasoning for this is quite simple, computing power at the race-track comes at a high cost and high risk. The racetrack is typically not at an urban spot, but at field conditions. 
Sending and receiving data over cellular networks is much easier than creating a local network with local computing power. 

## Component Design - suggestionGenerator
We have described all the data entities. We will now lay out the algorithms for the “online decision management module”. 
We will remind you that this module’s responsibility is getting all the calculated data about track entities, and run different algorithms on it. Each algorithm is responsible for one kind of decision making. 

#### Blue Flags Algorithm      
This algorithm is responsible for managing the display of blue flags, signaling a competitor to let another competitor pass. The logic follows these steps:

1. Identify the current leading lap number.
2. Identify all competitors with a lower lap count.
3. For each competitor with a lower lap count:
   - If the car immediately behind the competitor has a higher leading lap number and
   - If the car behind is less than X live gap in front,
   - Generate a blue flag notice for the competitor.
          
#### Yellow Flags Algorithm - 
This algorithm manages the yellow flags, which indicate a danger on the track. The algorithm works as follows:

1. For each competitor: 
   - If the speed of the competitor is less than X and
   - If the competitor's location is not in the pits,
   - Generate a yellow flag notice for this sector.

#### Location Monitor
This algorithm keeps track of the competitors' locations, particularly when they enter the pits. The logic follows these steps:

1. For each competitor: 
   - If the competitor's location is within the pits area and
   - If the competitor's speed is less than X,
   - Update the competitor's location status to 'pits'.

# Integration
We run the system in a real-world enviornment, according the project's goals, implementing this system is an easy and low-cost task. The first requirement is acquring an android phone for each competitor in the upcoming race. Then, initiate an AWS instance and clone this repository into it. Make sure to have the relevant ports open and available. Then use the `docker compose up` command to initiate the system and after 2-3 minutes it will be up and running. 

To start using the system, use a phone with the app to send the racetrack coordinates to the server. Enter the number `88888` to the app to "tell" the server that you're updating the racetrack GPS coordinates. After doing a single lap, turn-off the data transmition and then you're RACE READY! 
Assign a phone with the app to each competitor, enter the competitor's number to it. Then you can start the race and the data-driven race direction can begin! 
<p align="center">
<img width="480" alt="image" src="https://github.com/RazGavrieli/RaceControlServer/assets/90526270/2a0c9abc-92ca-44f8-affe-8d03b77614c3">
</p>

<p align="center">
Picture taken by Alex Lapiner at Arad Race Track (The Project’s Integration Enviorment).
</p>

# Tests
To test the system with real-world data, we have created scripts under the folder `tests`. The scripts there contain different scenarios that can be used to test the system. The idea for most of the test cases is the same, faking a competitor GPS data to fake a real race. The data that the tests use is stored in the folder `data`. This folder contains GPS coordinates for the racetrack and competitors. If you run the tests while the system is running, you fake a real race and the system will act as if it receives real data from real competitor. This means that we can test the generated suggestions. 
