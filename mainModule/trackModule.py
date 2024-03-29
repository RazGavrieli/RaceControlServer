import pika, threading
from objects.track import track

from enum import Enum
class TrackCommand(Enum):
    """Provides easy way to define the different commands given from a GPS module"""
    CREATE_TRACK = 88888
    SET_PITS = 99999
    SET_SECTOR = 77777
    MARSHEL_POST = 66666

class trackMod(threading.Thread):
    """
    This class provides a way to receive GPS data and update a `track` object accordingly.

    Attributes:
    RaceTrack : `track`
        A `track` object that holds all the information about the racetrack.
    """
    RaceTrack = track()
    
    trackQueueName = "TRACK"
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    TRACKchannel = connection.channel()
    TRACKchannel.queue_declare(queue=trackQueueName)

    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.TRACKchannel.basic_consume(queue=self.trackQueueName, on_message_callback=self.gps_callback, auto_ack=True)
    
    def run(self):
        print(' [*] Waiting for TRACK messages. To exit press CTRL+C')
        self.TRACKchannel.start_consuming()

    def get_racetrack(self) -> list:
        if len(self.RaceTrack.trackList) == 0:
            return [(0,0)]
    
        return self.RaceTrack.trackList
    
    def get_sectors(self) -> list:
        return self.RaceTrack.sectorsList
    
    def get_pits(self) -> list:
        return self.RaceTrack.pitsList
    
    def gps_callback(self, ch, method, properties, body):
        """
        A callback function that is called whenever a new message is received in the `track` queue.
        It updates the `RaceTrack` object accordingly based on the message content.
        """
        data = eval(body.decode())
        if data['id'] == TrackCommand.CREATE_TRACK.value:
            if data['latitude'] == 0 or data['longitude'] == 0:
                return
            print("adding point: ", data['latitude'], data['longitude'])
            self.RaceTrack.trackList.append((data['latitude'], data['longitude']))
        elif data['id'] == TrackCommand.SET_SECTOR.value:
            self.RaceTrack.sectorsList.append((data['latitude'], data['longitude']))
        elif data['id'] == TrackCommand.SET_PITS.value:
            self.RaceTrack.pitsList.append((data['latitude'], data['longitude']))
        elif data['id'] == TrackCommand.MARSHEL_POST.value:
            self.RaceTrack.marshelList.append((data['latitude'], data['longitude']))
#trackMod()