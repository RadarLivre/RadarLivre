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

        

<<<<<<< HEAD
def init():

    # Connect to collector
    connectCollector()
=======
    # Create the database folder if not exists
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)

    #Initializing the temporary database
    try:
        con = sql.connect(DATABASE_FILE_NAME)
        try:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS HexDataBase (Hex TEXT, Data TEXT, DateTime BIGINT);")
            con.commit()
        except sql.OperationalError, msg:
            print msg
            print "Error in insertion"
    except:
        print "Can't connect to local database"
        sys.exit(0)
>>>>>>> 2324a42c9ae8a4383bafeb48ce3ae5ef64b0b492

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

<<<<<<< HEAD
=======
def start():
    #Loop to capture and send data
>>>>>>> 2324a42c9ae8a4383bafeb48ce3ae5ef64b0b492
    while True:
        
        flag = not flag

        report.info("Waiting for receptor data...")
        line = s_com.readline()
        line = line[14:][:-2]
<<<<<<< HEAD
=======
        print "\n\nNew line: ", line
        try:
            SaveHex(line)  
        except:
            print "Error in save data"
>>>>>>> 2324a42c9ae8a4383bafeb48ce3ae5ef64b0b492

        report.info("New data received: " + line)

<<<<<<< HEAD
        db.save(line)  

        time.sleep(1)
    
=======
def SaveHex(HexData):
    ts = time.time()
    cur.execute("INSERT INTO HexDataBase (Hex, DateTime) VALUES('"+HexData+"', '"+str(ts)+"')")
    con.commit()
>>>>>>> 2324a42c9ae8a4383bafeb48ce3ae5ef64b0b492

def handler(signum, frame):

    serial.close()

