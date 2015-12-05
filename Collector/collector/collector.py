from threading import Thread
from uploader import start as start_collector
from adsb_capture import start as start_capture, init

def start():
	init()	

	print "Collector started"

	threadCapture = Thread(target = start_capture, args = ())
	threadCapture.start()

	threadCollector = Thread(target = start_collector, args = ())
	threadCollector.start()

	threadCapture.join()
	threadCollector.join()
