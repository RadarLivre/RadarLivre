#import gettext
import os 
from subprocess import call

LOCALE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'locale')

MSG_PROJECT_INFO = "Project"

MSG_SERVER_INIT_ON_PORT = "Server started on port:"
MSG_SERVER_CONNECTED_WITH = "Server connected with"
MSG_SERVER_DISCONNECTED_FROM = "Server disconnected from"

MSG_SERVER_INIT_ERROR = "Exception in server initialization:"
MSG_SERVER_ERROR = "Exception in server:"

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
