from threading import Thread
from uploader import start as start_collector

def start():
    print "Collector started"
    thread = Thread(target = start_collector, args = ())
    thread.start()
    thread.join()
