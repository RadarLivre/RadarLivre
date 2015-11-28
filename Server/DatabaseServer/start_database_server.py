from server import database_server
from server import translation
from server.translation import _, MSG_PROJECT_INFO

translation.initLanguages()

print _(MSG_PROJECT_INFO)
database_server.start()
