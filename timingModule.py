import requests
from bs4 import BeautifulSoup, element
import time
import pika
import sys
"""
Gets a speedhive's URL as parameter. (sys.argv[1]). 
Every UPDATE_INTERVAL seconds, checks for changes in the given URL. Send to 'TIMING' RabbitMQ's queue the changes. 
"""
if __name__=="__main__":
    if len(sys.argv) != 2:
        raise BaseException("please enter timing URL")
    URL = sys.argv[1]
    UPDATE_INTERVAL = 0.25
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', socket_timeout=None))
    channel = connection.channel()
    channel.queue_declare(queue='TIMING')
    lastDict = {}
    while True:
        try:
            response = requests.get(URL)
        except:
            print("http error")
        soup = BeautifulSoup(response.content, "html.parser")
        resultsList = soup.find("div", {"class": "results-list"})

        for row in resultsList:
            if type(row) == element.Tag:
                number = row.find("div", {"class": "number"}).text
                laps = row.find("div", {"class": "laps"}).text
                position = row.find("div", {"class": "position"}).find("span", {"class": "value"}).text
                compDict = {'id': number, 'laps': laps, 'pos': position}
                if number in lastDict.keys() and lastDict[number] == compDict:
                    pass
                else:
                    lastDict[number] = compDict
                    channel.queue_declare(queue='TIMING')
                    channel.basic_publish(exchange='', routing_key='TIMING', body=str(compDict))
                    print(compDict)
        
        time.sleep(UPDATE_INTERVAL)
