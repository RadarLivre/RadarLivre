import serial

from server.translation import _, MSG_COLLECTOR_INIT,\
    MSG_COLLECTOR_WRITE_DATA_GET_VERSION, MSG_COLLECTOR_WRITE_DATA_START,\
    MSG_COLLECTOR_RECEIVING_MESSAGE, MSG_COLLECTOR_RETURN,\
    MSG_COLLECTOR_CANT_START
from server.decoder.adsb_decoder import ADSBDataDecoder
from config import COLLECTOR_ADDRESS

def start():
    
    print _(MSG_COLLECTOR_INIT)
    
    try: 
        ser = serial.Serial(COLLECTOR_ADDRESS, 115200, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, xonxoff=False, rtscts=False, dsrdtr=False)
        
        ser.write("#00\r\n")
        print _(MSG_COLLECTOR_WRITE_DATA_GET_VERSION)
        k = ser.readline()  
        print _(MSG_COLLECTOR_RETURN) + str(k)
        
        ser.write("#43-02\r\n") 
        print _(MSG_COLLECTOR_WRITE_DATA_START)
        k = ser.readline()
        
        while True:
            k = ser.readline()
            k = k[14:][:-2]
            print "\n\n\n", _(MSG_COLLECTOR_RECEIVING_MESSAGE)
            print str(k)
            ADSBDataDecoder(str(k))
        
    except Exception:
        print _(MSG_COLLECTOR_CANT_START), COLLECTOR_ADDRESS
