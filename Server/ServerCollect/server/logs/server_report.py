'''
  Tipos:
  0 - General Exception
  1 - Alerta
  2 - Queda
'''

from datetime import datetime
import os
from config import DEFAULT_LOG_DIR, DEFAULT_FILE_NAME_SERVER_REPORT

LOCALE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR = os.path.join(LOCALE_PATH, DEFAULT_LOG_DIR)

def report(module, type, msg):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    f = file(os.path.join(LOG_DIR, DEFAULT_FILE_NAME_SERVER_REPORT), 'a')
    now = datetime.now()
    f.write(str(now) + " - "+module+" - "+type+" - "+msg+"\n")
    f.close()
