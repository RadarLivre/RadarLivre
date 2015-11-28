# -*- coding: utf-8 -*-

import psycopg2
import sys
import json
import time

try:
    con2 = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='radar')
    cur2 = con2.cursor()
except Exception as ex:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    print ex
    sys.exit(0)

results = []
hexIcao = []

def findArray(zi):
    for i in hexIcao:
        if i == zi:
            return True
    return False

def get_realtime_airplane_list():
    cur2.execute("SELECT * FROM HexDataBase AS A INNER JOIN (SELECT MAX(timestamp) as timestamp, hexicao FROM hexdatabase GROUP BY hexicao) AS B ON A.timestamp = B.timestamp AND A.hexicao = B.hexicao");

    columns = (
        'id_reg', 'timestamp', 'hex', 'icao', 'id', 'latitude', 'longitude', 'altitude', 'climb', 'head', 'velocidadegnd', 'utf' 
    )

    values = cur2.fetchall();
    
    # Apenas as aeronaves atualizadas a menos de um minuto são retornadas
    currentTime = int(time.time());
    results = filter(lambda x: x[1] >= (currentTime - 1000000000), values)

    s = [];
    for resultz in results:
        s.append(dict(zip(columns, resultz)))

    del results[:]
    del hexIcao[:]
    resultz = []    

    return json.dumps(s, indent=2)

def get_airplane_track(planehex):
    cur2.execute("SELECT * FROM HexDataBase WHERE hexicao = '"+str(planehex)+"' ORDER BY timestamp ASC")

    columns = (
        'id_reg', 'timestamp', 'hex', 'icao', 'id', 'latitude', 'longitude', 'altitude', 'climb', 'head', 'velocidadegnd', 'utf'
    )

    results = []
    for row in cur2.fetchall():
    	results.append(dict(zip(columns, row)))

    index = 0
    for i in range(0, len(results) - 1):
    	r1 = results[i];
    	r2 = results[i + 1];

    	print (r2["timestamp"] - r1["timestamp"]), " ", 
    	if r2["timestamp"] - r1["timestamp"] >= 60:
    		index = i + 1;

    return json.dumps(results[index : len(results)], indent=2)

def search_flight(FlightName):
    cur2.execute("SELECT * FROM HexDataBase WHERE id_ = '"+str(FlightName)+"' ORDER BY timestamp DESC LIMIT 1")

    columns = (
     'hex', 'latitude', 'longitude'
    )

    results = []
    for row in cur2.fetchall():
         results.append(dict(zip(columns, row)))
    return json.dumps(results, indent=2)

def get_list_airports():
    cur2.execute("SELECT * FROM airportlist")
    #timestamp, hexicao, icao, callsign, lat, lon, alt, climb, head, velocidadegnd, utf
    columns = (
     'icao', 'name', 'state', 'city', 'latitude', 'longitude' 
    ) #inclinacao, angulo, origem

    results = []
    for row in cur2.fetchall():
         results.append(dict(zip(columns, row)))
    return json.dumps(results, indent=2)
