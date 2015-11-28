# import gettext
import os 
from subprocess import call

LOCALE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'locale')

MSG_PROJECT_INFO = "Project"

MSG_SERVER_INIT_ON_PORT = "Server started on port:"
MSG_SERVER_CANT_START_ON_PORT = "Can't start server on port:"
MSG_COLLECTOR_INIT = "Collector started"
MSG_COLLECTOR_WRITE_DATA_GET_VERSION = "Write data: Get Version"
MSG_COLLECTOR_WRITE_DATA_START = "Write data: Start"
MSG_COLLECTOR_RECEIVING_MESSAGE = "Receiving message"
MSG_COLLECTOR_RETURN = "Return: "
MSG_COLLECTOR_CANT_START = "Can't start collector with address:"

MSG_READ_LOGS = "Reading logs"

LANGUAGE = None

def initLanguages():
    '''
    try:
        for dirname, dirnames, filenames in os.walk(LOCALE_PATH):
            for filename in filenames:
                path = os.path.join(dirname, filename)
                if ".po" in path:
                    call(["msgfmt", path])
                    call(["mv", "messages.mo", dirname + "/translation.mo"])
    except:
        pass
    global LANGUAGE
    try:     
        LANGUAGE = gettext.translation("translation", LOCALE_PATH, languages=["pt", "en"])
        LANGUAGE.install()
    except:
        LANGUAGE = gettext
    
    '''
def _(msg):
    #return LANGUAGE.gettext(msg)
    return msg
