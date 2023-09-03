# -*- coding: utf-8 -*-

# psql -U postgres -h localhost -d radarlivre_v4 -f out.sql

import io
import re
import sys
import numbers
from time import time as now

total = 0
progress = 0

patternCommas = "(\"[^\n\",]+)((,)([^\",]*))+([^\n\",]*\")"
patternQuotes = "\"(.*?)\""
patternDoubleQuotes = "\"\"([^\"]*)\"\""

def showStatus(prefix):
    if progress == total:
        print ("\nFinish!")
    else:
        x = int(progress * 20 / total)

        out = "" + prefix + ": ["
        for i in range(0, 20):
            if(i < x):
                out += "#"
            elif i == x:
                out += ">"
            else:
                out += " "
        print ("\r"),
        print (out + "] " + str(progress) + " of " + str(total)),

def getObjects(fileName):
    global progress
    progress = 0
    global total

    objects = []

    file = io.open(fileName, encoding="UTF-8")
    lines = file.read().split("\n")
    file.close()
    headers = lines[0].split(",")
    rows = lines[1:]

    total = len(rows)

    for row in rows:
        progress += 1

        tmp = row
        row = re.sub(patternDoubleQuotes, "@!DOUBLEQUOTES!@\\1@!DOUBLEQUOTES!@", row)
        row = re.sub(patternCommas, "\\1@!COMMA!@\\4\\5", row)
        tmp2 = row
        row = row.split(",")

        if  len(row) == len(headers):
            object = {}
            for header, attr in zip(headers, row):
                header = re.sub(patternQuotes, "\\1", header)
                attr = re.sub(patternQuotes, "\\1", attr)
                attr = re.sub("@!DOUBLEQUOTES!@", "\"\"", attr)
                attr = re.sub("@!COMMA!@", ",", attr)
                attr = re.sub("'", "''", attr)
                attr = re.sub("\"", "\"\"", attr)
                attr = attr.replace("\N", "")
                object[header] = attr

            objects.append(object)
        else:
            print (len(row), ":", len(headers), ":", tmp)
            print (len(row), ":", len(headers), ":", tmp2)

        showStatus(fileName)

    return objects

def getByCode(objects, code):
    for o in objects:
        if o["code"] == code:
            return o
    return None

def parseNumber(n):
    try:
        float(n)
        return n
    except ValueError:
        print (n)
        return 0

def encode(text):
    return text.encode('utf-8')

def generateAirportSQL():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    airports = getObjects("airports.csv")
    countries = getObjects("countries.csv")
    regions = getObjects("regions.csv")

    global progress
    progress = 0
    global total
    total = len(airports)

    out = "BEGIN\n"

    for airport in airports:
        country = getByCode(countries, airport["iso_country"])
        region = getByCode(regions, airport["iso_region"])

        sql = "INSERT INTO radarlivre_api_airport (code, name, country, state, city, latitude, longitude, type) VALUES({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7});\n".format(
            ("'" + str(airport["ident"]) + "'"), ("'" + str(airport["name"]) + "'"),
            ("'" + str(country["name"] + "'")) if country else "NULL", ("'" + str(region["name"]) + "'") if region else "NULL", ("'" + str(airport["municipality"]) + "'"),
            parseNumber(str(airport["latitude_deg"])), parseNumber(str(airport["longitude_deg"])),
            ("'" + str(airport["type"]) + "'")
        )
        out += sql

        progress += 1
        showStatus("Generating Airport SQL")

    out += "COMMIT"

    file = open("airport.sql", "w")
    file.write(out)
    file.close()

    print ("SQL generated!")

def generateAirlineSQL():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    airlines = getObjects("airlines.csv")

    global progress
    progress = 0
    global total
    total = len(airlines)

    out = "BEGIN\n"

    for airline in airlines:

        sql = "INSERT INTO radarlivre_api_airline (name, alias, iata, icao, callsign, country, active) VALUES({0}, {1}, {2}, {3}, {4}, {5}, {6});\n".format(
            ("'" + str(airline["name"]) + "'"), ("'" + str(airline["alias"]) + "'"),
            ("'" + str(airline["iata"]) + "'"), ("'" + str(airline["icao"]) + "'"), ("'" + str(airline["callsign"]) + "'"),
            ("'" + str(airline["country"]) + "'"), ("'" + str(airline["active"]) + "'")
        )
        out += sql

        progress += 1
        showStatus("Generating Airline SQL")

    out += "COMMIT"

    file = open("airline.sql", "w")
    file.write(out)
    file.close()

    print ("SQL generated!")

timestamp = now()

generateAirlineSQL()
generateAirportSQL()

print ("time:", (now() - timestamp))