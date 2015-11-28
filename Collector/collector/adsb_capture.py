import sys
import sqlite3 as sql
import datetime
import time
import serial
import json
import signal
import os

from config import COLLECTOR_ADDRESS, DATABASE_DIR, DATABASE_FILE

DATABASE_FILE_NAME = os.path.join(DATABASE_DIR, DATABASE_FILE)

def start():

    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)

    #Inicia Serial
    try:
        s_com = serial.Serial(COLLECTOR_ADDRESS, 115200, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, xonxoff=False, rtscts=False, dsrdtr=False)
    except Exception as ex:
        print ex
        print "Can't connect ro receptor"
        sys.exit(0)

    #Inicia Banco de Dados Temporario
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
        print "Can't connecto to local database"
        sys.exit(0)


    signal.signal(signal.SIGINT, handler)

    print("Getting receptor version")
    s_com.write("#00\r\n")
    k = s_com.readline()  
    print "Return from Receptor: " + str(k)

    print("Initializing data receiving...")
    s_com.write("#43-02\r\n")
    k = s_com.readline()
    print "Return from Receptor: "+str(k)

    print "Capture mode has been initialized"

    #Loop Captura e envio dos Dados
    while True:
        line = s_com.readline()
        line = line[14:][:-2]
        print line
        try:
         SalvaHex(line)  
        except:
         print "Error in save data"


def SalvaHex(HexData):
    ts = time.time()
    cur.execute("INSERT INTO HexDataBase (Hex, DateTime) VALUES('"+HexData+"', '"+str(ts)+"')")
    con.commit()

def handler(signum, frame):
    serial.close()

