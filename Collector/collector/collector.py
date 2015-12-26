from threading import Thread
from uploader import start as start_upload
from adsb_capture import start as start_capture, init as init_capture_resources

def start():
	init_capture_resources()
	
	threadCapture = Thread(target = start_capture, args = ())
	threadCapture.start()

	threadUploader = Thread(target = start_upload, args = ())
	threadUploader.start()

	threadCapture.join()
	threadUploader.join()
