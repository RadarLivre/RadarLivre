from simple_websocket_server import WebSocket, SimpleWebSocketServer
from server.http_server_database import get_realtime_airplane_list, get_list_airports,\
    get_airplane_track, search_flight
from server.translation import MSG_SERVER_INIT_ON_PORT, MSG_SERVER_INIT_ERROR,\
    MSG_SERVER_ERROR, MSG_SERVER_CONNECTED_WITH, MSG_SERVER_DISCONNECTED_FROM

class ADSBDataEcho(WebSocket):

        def handleMessage(self):
            if self.data == 'GET_AIRPLANES':
                try:
                        self.sendMessage("GET_AIRPLANES_RESPONSE:" + str(get_realtime_airplane_list()))
                except Exception as ex:
                        print _(MSG_SERVER_ERROR), str(ex)

            elif self.data == 'GET_AIRPORTS':
                try:
                        self.sendMessage("GET_AIRPORTS_RESPONSE:" + str(get_list_airports()))
                except Exception as ex:
                        print _(MSG_SERVER_ERROR), str(ex)

            elif 'GET_ROUTE(' in self.data:
                icao = self.data.replace("GET_ROUTE(", "")
                icao = icao.replace(")", "")
                try:
                        self.sendMessage("GET_ROUTE_RESPONSE:" + str(get_airplane_track(icao)))
                except Exception as ex:
                        print _(MSG_SERVER_ERROR), str(ex)

            elif 'SEARCH(' in self.data:
                    FlightName = self.data.replace("SEARCH(", "")
                    FlightName = FlightName.replace(")", "")
                    self.sendMessage("SEARCH_RESPONSE:" + search_flight(FlightName))

        def handleConnected(self):
            print _(MSG_SERVER_CONNECTED_WITH), self.address

        def handleClose(self):
            print _(MSG_SERVER_DISCONNECTED_FROM), self.address

def start():
    try:
        server = SimpleWebSocketServer('', 9999, ADSBDataEcho)
        print _(MSG_SERVER_INIT_ON_PORT), "9999"
        server.serveforever()
    except Exception as ex:
        print _(MSG_SERVER_INIT_ERROR), str(ex)
