import os
import datetime
from config import LOG_DIR

LOCALE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(LOCALE_PATH, LOG_DIR)

LOG_FILE_INFO = "info.log"
LOG_FILE_ERROR = "error.log"
LOG_FILE = "report.log"

def setupLogDir():

	if not os.path.exists(LOG_DIR):
		os.makedirs(LOG_DIR)

def setupLogFile():

	setupLogDir()
	logFilePath = os.path.join(LOG_DIR, LOG_FILE)
	logFile = open(logFilePath, 'a')
	return logFile


def setupLogFileInfo():

	setupLogDir()
	logFilePath = os.path.join(LOG_DIR, LOG_FILE_INFO)
	logFile = open(logFilePath, 'a')
	return logFile


def setupLogFileError():
	
	setupLogDir()
	logFilePath = os.path.join(LOG_DIR, LOG_FILE_ERROR)
	logFile = open(logFilePath, 'a')
	return logFile


def info(message):
	logi = setupLogFileInfo()
	logi.write(str(datetime.datetime.now()) + " - " + message + "\n\n")
	logi.close()
	log(message)


def error(message):
	loge = setupLogFileError()
	loge.write(str(datetime.datetime.now()) + " - " + message + "\n\n")
	loge.close()
	log(message)

def log(message):
	log = setupLogFile()
	log.write(str(datetime.datetime.now()) + " - " + message + "\n\n")
	log.close()

	print str(datetime.datetime.now()) + " - " + message + "\n"

