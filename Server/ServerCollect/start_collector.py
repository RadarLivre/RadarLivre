from server import translation
from server.collector import local_collector
from server.translation import _
from server.translation import MSG_PROJECT_INFO

translation.initLanguages()

local_collector.start();