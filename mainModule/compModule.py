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
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue=gpsQueueName)
    channel.queue_declare(queue=timingQueueName)

    def __init__(self) -> None:
        """
        Constructor method that initializes the object and starts listening to the GPS and TIMING queues.
        """
        threading.Thread.__init__(self)
        self.channel.basic_consume(queue=self.gpsQueueName, on_message_callback=self.callback, auto_ack=True)
        self.channel.basic_consume(queue=self.timingQueueName, on_message_callback=self.callback, auto_ack=True)

    def run(self):
        print(' [*] Waiting for TIMING & GPS messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def get_competitor(self, id) -> competitor:
        if id not in self.competitors:
            return competitor(id)
        return self.competitors[id]

    def callback(self, ch, method, properties, body):
        if "queue_name" in properties.headers:
            if properties.headers["queue_name"] == self.gpsQueueName:
                # Process message from GPS Queue
                self.GPS_process(body)

            elif properties.headers["queue_name"] == self.timingQueueName:
                # Process message from TIMING Queue
                self.TIMING_process(body)
        else:
            # Handle messages without the 'queue_name' header
            print("no header")

    def GPS_process(self, body):
        """
        Callback method that processes GPS data received from the GPS queue.
        """
        data = eval(body.decode())
        compid = str(data['id'])
        if compid == 0:
            # TODO CODE FOR SC
            pass
        elif compid in self.competitors:
            self.competitors[compid].lastknownGPS = (data['latitude'], data['longitude'])
            self.competitors[compid].lastKnownSpeed = data['speed']
            self.competitors[compid].lastKnownGforce = data['gForce']
        else:
            newCompetitor = competitor(compid)
            newCompetitor.lastknownGPS = (data['latitude'], data['longitude'])
            newCompetitor.lastKnownSpeed = data['speed']
            newCompetitor.lastKnownGforce = data['gForce']
            self.competitors[compid] = newCompetitor


    def TIMING_process(self, body):
        """
        Callback method that processes timing data received from the timing queue.
        """
        data = eval(body.decode())
        compid = str(data['id'])
        if compid in self.competitors:
            self.competitors[compid].lastKnownLap = data['laps']
            self.competitors[compid].lastKnownPos = data['pos']
        else:
            newCompetitor = competitor(compid)
            newCompetitor.lastKnownLap = data['laps']
            newCompetitor.lastKnownPos = data['pos']
            self.competitors[compid] = newCompetitor



#compMod()