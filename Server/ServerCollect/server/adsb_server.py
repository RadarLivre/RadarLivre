import json
from socket import *
from server.decoder.adsb_decoder import ADSBDataDecoder
from translation import _
from server.translation import MSG_SERVER_INIT_ON_PORT, MSG_SERVER_CANT_START_ON_PORT
from server.logs.server_report import report
import select


def start():
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 
    PORT = 5000

    try:
        server_socket = socket()
        server_socket.bind(("localhost", PORT))
        server_socket.listen(10)
        CONNECTION_LIST.append(server_socket)
        
        print _(MSG_SERVER_INIT_ON_PORT) + " " + str(PORT)
        
    except Exception as ex:
        report('adsbServidor', '0', str(ex))
        print _(MSG_SERVER_CANT_START_ON_PORT) + " " + str(PORT)
 
    while True:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        try:
                            if 'Online: ' not in data:
                                #PyAdsbDecoderDatabase.DumpColetores(data)
                                dp = json.loads(data)
                                print data
                            
                                if dp[3] == 'ADSBHEXDATA':

                                    # Obter Timestamp Frame vindo do Coletor
                                    # Obter Lat e Long o Coletor e repassar para o DataDecoder
                                    
                                    dp2 = json.loads(dp[0]) #obtem o conteudo do pacote
                                    for z in dp2:
                                        ADSBDataDecoder(z[0])

                                if dp[3] == 'JSONDATA':
                                    print "Nao implementado"
                                        
                        except Exception as ex:
                            print ex
                            
                except:
                    print "Client (%s, %s) is offline" % addr
                    report('adsbServidor', '2', 'Queda de Conexao com Coletor - '+str(addr))
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
         
    server_socket.close()
