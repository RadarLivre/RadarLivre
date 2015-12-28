import os
import socket
import time
import sqlite3 as sql
import json
import database as db
import httplib, urllib2 as urllib
import report
from adsb import decoder

from config import LATITUDE,\
    LONGITUDE

from config import COLLECTOR_ADDRESS, DATABASE_DIR, DATABASE_FILE, DECODE_BEFORE_SEND

LOCALE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(LOCALE_PATH, DATABASE_DIR)
DATABASE_FILE_NAME = os.path.join(DATABASE_DIR, DATABASE_FILE)

## New

def sendJson(host, json):
    resp = None
    conn = None

    try:

        req = urllib.Request(host) 
        req.add_header("Content-type", "application/json")
        
        resp = urllib.urlopen(req, json)

    except Exception as e:

        report.error("Error while send data to server: " + str(e) + "\n" + str(json))

    finally:
            
        if conn:

            conn.close()

def sendMessagesToServer(messages):

    report.info("Sending collected data to server: " + str(len(messages)) + " messages")

    host = "http://52.27.151.5/api/"

    for m in messages:

        if DECODE_BEFORE_SEND:

            halfObservation = decoder.decodeMessage(m)

            if halfObservation:
                jsonMessage = json.dumps(halfObservation.serialize())

                host += "half_observation/"

                sendJson(host, jsonMessage)            

        else:

            jsonMessage = json.dumps(m)

            host += "adsb_message/"

            sendJson(host, jsonMessage)


def start():

    while True:

        time.sleep(1)

        rawMessages = db.getAll()

        if not rawMessages:

            # Nothing to sent
            pass

        elif len(rawMessages) == 0:

            # Nothing to sent
            pass

        else:

            messages = []

            for m in rawMessages:

                data = m[0]
                
                message = {
                    "latitude": str(LATITUDE), 
                    "longitude": str(LONGITUDE), 
                    "data": str(data), 
                }

                messages.append(message)

            sendMessagesToServer(messages)
            for m in rawMessages:
                db.removeFromTimestamp(m[1])


## Old
