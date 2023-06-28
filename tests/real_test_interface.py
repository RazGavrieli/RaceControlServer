import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='TIMING')
comps = {}

while True:
    # get number input from console
    try:
        compNumber = int(input("Enter competitor number: "))
    except ValueError:
        print("Please enter a valid number")
        continue

    if compNumber in comps.keys():
        comps[compNumber][0]['laps'] += 1
        comps[compNumber][1] = time.time()
    else:
        comps[compNumber] = [{'id': compNumber, 'laps': 1, 'pos': len(comps)+1}, time.time()]

    # sort by laps and then by time, and update positions - the one with the most laps is first, and if two competitors have the same amount of laps, the one with the lower time is first
    comps = dict(sorted(comps.items(), key=lambda x: (x[1][0]['laps'], x[1][1]), reverse=True))
    for index, i in enumerate(comps):
        comps[i][0]['pos'] = index+1

    channel.basic_publish(exchange='', routing_key='TIMING', body=str(comps[compNumber][0]), properties=pika.BasicProperties(headers={"queue_name": "TIMING", "additional_property": "value"}))
    print("Sent: ", comps[compNumber], "\nCurrent Standings: ", comps)