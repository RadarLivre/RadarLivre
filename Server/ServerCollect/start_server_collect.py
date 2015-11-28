from server import translation, adsb_server
from server.translation import _
from server.translation import MSG_PROJECT_INFO

translation.initLanguages()

print _(MSG_PROJECT_INFO)
adsb_server.start()



