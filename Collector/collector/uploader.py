import socket
import time
import sqlite3 as sql
import json
from config import SERVER_ADDRESS, PORT, COLLECTOR_ID, DATA_FORMAT, LATITUDE,\
    LONGITUDE

con = None
cur = None

def LimpaHex(limiteTS):
    cur.execute("DELETE FROM HexDataBase WHERE DateTime < '" +str(limiteTS)+"'")
    con.commit()

def TryConnect():
    while(True):
        lastid = 0
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_ADDRESS, PORT))
            print "Connected!"
            while True:
                cur.execute("SELECT * FROM HexDataBase")
                con.commit()
                recs = cur.fetchall()
                if str(recs) != '[]':
                    for k in recs:
                        lastid = k[0]
                    dt = time.time()
                    array_send = [json.dumps(recs), dt, COLLECTOR_ID, DATA_FORMAT, LATITUDE, LONGITUDE]
                    senddata = str(json.dumps(array_send))
                    try:
                        print "Sending data..."
                        client_socket.send(senddata)
                        LimpaHex(lastid)
                    except Exception as ex:
                        if "no such table:" not in str(ex):
                            print ex
                            break
                        else:
                            client_socket.close()
                            break
                else:
                    print "Waiting for data..."
                    try:
                        client_socket.send('Online: ' + COLLECTOR_ID)
                    except:
                        client_socket.close()
                        break
                time.sleep(0.5)
                
        except Exception as ex:
            if "no such table:" in str(ex):
                print "Error in DB: "+str(ex)
                print "Connection finish"
                client_socket.close()
            else:
                print ex
                print "Can't connect to server... try again in 5 sec..."
                time.sleep(5)
                client_socket.close()
                
             
def start():
    global con, cur
    con = sql.connect('datadumptemp.db')
    try:
        cur = con.cursor()
        con.commit()
    except sql.OperationalError, msg:
        print msg
        print "Erro in dabase insertion"
        exit()
        
    TryConnect()