import os
import sys
import report
import sqlite3 as sql
import time

from config import DATABASE_DIR, DATABASE_FILE

LOCALE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(LOCALE_PATH, DATABASE_DIR)
DATABASE_FILE_NAME = os.path.join(DATABASE_DIR, DATABASE_FILE)

def setupDatabaseDir():
    
    # Create the database dir if not exists
    if not os.path.exists(DATABASE_DIR):

        os.makedirs(DATABASE_DIR)

def executeQuery(query):

    result = None

    setupDatabaseDir()

    con = None

    try:

        con = sql.connect(DATABASE_FILE_NAME)

        try:

            cur = con.cursor()
            cur.execute(query)
            con.commit()
            result = cur.fetchall()
            cur.close()

        except sql.OperationalError, msg:

            report.error("Can't execute query: " + str(msg))

    except sql.Error, e:

        report.error("Can't connect to local database: " + str(e))

    finally:
    
        if con:

            con.close()

    return result

def init():

    report.info("Opening local database")

    # Create the database dir if not exists
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)

    executeQuery("CREATE TABLE IF NOT EXISTS ADSB_MESSAGE (MESSAGE TEXT, _TIMESTAMP BIGINT)")
    
    

def save(data):

    report.info("Saving data received")

    executeQuery("INSERT INTO ADSB_MESSAGE (MESSAGE, _TIMESTAMP) VALUES('" + data + "', '" + str(time.time()) + "')")


def getAll():
    return executeQuery("SELECT * FROM ADSB_MESSAGE")

def removeFromTimestamp(timestamp):
    executeQuery("DELETE FROM ADSB_MESSAGE WHERE _TIMESTAMP = " + str(timestamp))