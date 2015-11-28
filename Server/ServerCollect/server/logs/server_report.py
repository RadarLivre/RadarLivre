'''
  Tipos:
  0 - General Exception
  1 - Alerta
  2 - Queda
'''

from datetime import datetime
import os
from config import DEFAULT_LOG_DIR, DEFAULT_FILE_NAME_SERVER_REPORT

def report(module, type, msg):
    if not os.path.exists(DEFAULT_LOG_DIR):
        os.makedirs(DEFAULT_LOG_DIR)
    
    f = file(DEFAULT_FILE_NAME_SERVER_REPORT, 'a')
    now = datetime.now()
    f.write(str(now) + " - "+module+" - "+type+" - "+msg+"\n")
    f.close()
