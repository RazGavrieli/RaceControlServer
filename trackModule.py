import pika
from objects.track import track

from enum import Enum
class TrackCommand(Enum):
    """Provides easy way to define the different commands given from a GPS module"""
    CREATE_TRACK = 88888
    SET_PITS = 99999
    SET_SECTOR = 77777
    MARSHEL_POST = 66666

class trackMod:
    """
    This class provides a way to receive GPS data and update a `track` object accordingly.

    Attributes:
    RaceTrack : `track`
        A `track` object that holds all the information about the racetrack.
    """
    RaceTrack = track()
    
    trackQueueName = "TRACK"
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    TRACKchannel = connection.channel()
    TRACKchannel.queue_declare(queue=trackQueueName)

    def __init__(self) -> None:
        self.TRACKchannel.basic_consume(queue=self.trackQueueName, on_message_callback=self.gps_callback, auto_ack=True)
        print(' [*] Waiting for TRACK messages. To exit press CTRL+C')
        self.TRACKchannel.start_consuming()

    def gps_callback(self, ch, method, properties, body):
        """
        A callback function that is called whenever a new message is received in the `track` queue.
        It updates the `RaceTrack` object accordingly based on the message content.
        """
        data = body.encode()
        if data['id'] == TrackCommand.CREATE_TRACK.value:
            self.RaceTrack.trackList.append(data['latitude'], data['longitude'])
        elif data['id'] == TrackCommand.SET_SECTOR.value:
            self.RaceTrack.sectorsList.append(data['latitude'], data['longitude'])
        elif data['id'] == TrackCommand.SET_PITS.value:
            self.RaceTrack.pitsList.append(data['latitude'], data['longitude'])
        elif data['id'] == TrackCommand.MARSHEL_POST.value:
            self.RaceTrack.marshelList.append(data['latitude'], data['longitude'])
            
trackMod()