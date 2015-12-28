import sys
import datetime
import time
import serial
import json
import signal
import os
import report
import database as db

from config import COLLECTOR_ADDRESS

s_com = None

def connectCollector():

    report.info("Connecting to collector " + COLLECTOR_ADDRESS)

    global s_com

    try:

        s_com = serial.Serial(COLLECTOR_ADDRESS, 115200, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, xonxoff=False, rtscts=False, dsrdtr=False)
        report.info("Conected with collector!")

    except Exception as ex:

        report.error("Can't connect to receptor: " + str(ex))

        sys.exit(0)

        
def init():

    # Connect to collector
    connectCollector()

    # Initialize database
    db.init()

    signal.signal(signal.SIGINT, handler)

def start():
    
    s_com.write("#00\r\n")
    k = s_com.readline()  
    report.info("Receptor version: \n" + str(k))

    s_com.write("#43-02\r\n")
    k = s_com.readline()
    report.info("Initializing data receiving: \n" + str(k))

    report.info("Capture mode has been initialized")

    msgs = open("msg.txt", "r")
    msgs = msgs.read()
    msgs = msgs.split("\n\n")
    index = 0

    while index < len(msgs):

        report.info("Waiting for receptor data...")
        #line = s_com.readline()
        #line = line[14:][:-2]

        line = msgs[index]
        index += 1
        
        report.info("New data received: " + line)

        db.save(line)  

        time.sleep(2)

def handler(signum, frame):

    serial.close()
