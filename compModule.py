import pika, threading
from objects.competitor import competitor

class compMod(threading.Thread):
    """
    The `compMod` class is responsible for receiving and processing GPS and timing data for competitors in a race.
    It manages a dictionary of competitor object, which is getting updated with the data received.

    Attributes:
    - competitors: A dictionary containing competitor objects, with competitor IDs as keys.

    Methods:
    - __init__(): Constructor method that initializes the object and starts listening to the GPS and timing queues.
    - gps_callback(): Callback method that processes GPS data received from the GPS queue.
    - timing_callback(): Callback method that processes timing data received from the timing queue.
    """
    competitors = {}

    gpsQueueName = 'GPS'
    timingQueueName = 'TIMING'
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    GPSchannel = connection.channel()
    GPSchannel.queue_declare(queue=gpsQueueName)
    TIMINGchannel = connection.channel()
    TIMINGchannel.queue_declare(queue=timingQueueName)

    def __init__(self) -> None:
        """
        Constructor method that initializes the object and starts listening to the GPS and timing queues.
        """
        threading.Thread.__init__(self)

        self.GPSchannel.basic_consume(queue=self.gpsQueueName, on_message_callback=self.gps_callback, auto_ack=True)
        self.TIMINGchannel.basic_consume(queue=self.timingQueueName, on_message_callback=self.timing_callback, auto_ack=True)



    def run(self):
        print(' [*] Waiting for TRACK & GPS messages. To exit press CTRL+C')
        self.GPSchannel.start_consuming()
        self.TIMINGchannel.start_consuming()

    def gps_callback(self, ch, method, properties, body):
        """
        Callback method that processes GPS data received from the GPS queue.
        """
        data = eval(body.decode())
        if data['id'] in self.competitors:
            self.competitors[data['id']].lastknownGPS = (data['latitude'], data['longitude'])
            self.competitors[data['id']].lastKnownSpeed = data['speed']
            # TODO add gForce
        else:
            newCompetitor = competitor(data['id'])
            newCompetitor.lastknownGPS = (data['latitude'], data['longitude'])
            newCompetitor.lastKnownSpeed = data['speed']
            # TODO add gForce
            self.competitors[data['id']] = newCompetitor

        print(self.competitors[data['id']])

    def timing_callback(self, ch, method, properties, body):
        """
        Callback method that processes timing data received from the timing queue.
        """
        data = eval(body.decode())
        if data['id'] in self.competitors:
            self.competitors[data['id']].lastKnownLap = data['laps']
            self.competitors
