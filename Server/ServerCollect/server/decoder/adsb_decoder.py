#
# PyADS-B Decoder in Python
# Felipe Sousa Rocha, 01/08/2014
#

import math
from server.math_utils.crc_calc import *
from server.math_utils.adsb_decoder_library import *
from server.database.adsb_decoder_database import *

# Aircraft Type
cs_tbl = ['@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
          'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', ' ', ' ', ' ', ' ',
          ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', ' ', ' ', ' ', ' ', ' ']

def ADSBDataDecoder(data, showStatus = True, dumpOnDatabase = True, latHome = -4.864790, lonHome = -39.580930):

    if len(data) == 28:
       print "Pacote 112: Bits"
       if parity112(data) == False:
          print "CRC - Invalido!"
          return False
       else:
           print "CRC - Valido!"
        
       ICAO = data[2]+data[3]+data[4]+data[5]+data[6]+data[7] #Da pra reduzir
       DFCA = toHex(data[:2]) #Da pra reduzir
       DF = full_bit_zero(bin(eval(DFCA)))[:5] #Da pra reduzir
       DF = eval("0b" + DF) #Da pra reduzir
       CA = full_bit_zero(bin(eval(DFCA)))[5:] #Da pra reduzir
       b_TC = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[:5] #Da pra reduzir
       TC = eval("0b"+b_TC)  #Da pra reduzir
       b_Mode = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[5:] #Tres bits para o mode
      
       if DF == 17:
           print 'Downlink Format: 17 - S Mode'
           if FindICAOExists(ICAO) == False:
              CreateAirplane(ICAO)
              print "Novo Airplane Criado: " + str(ICAO)

           if TC >= 1 and TC <= 4:
               print "Type: Airplane Identification Message... (Nome do Voo, Tipo Aeronave)"
               hex_adsb_packet = data[8:] #Da pra reduzir
               bin_adsb_packet = c(hex_adsb_packet[0],hex_adsb_packet[1])+c(hex_adsb_packet[2],hex_adsb_packet[3])+c(hex_adsb_packet[4],hex_adsb_packet[5])+c(hex_adsb_packet[6],hex_adsb_packet[7])+c(hex_adsb_packet[8],hex_adsb_packet[9])+c(hex_adsb_packet[10],hex_adsb_packet[11])+c(hex_adsb_packet[12],hex_adsb_packet[13])
               
               formattypecode = bin_adsb_packet[0] + bin_adsb_packet[1] + bin_adsb_packet[2] + bin_adsb_packet[3] + bin_adsb_packet[4] #Da pra reduzir
               aircrafttype = bin_adsb_packet[5] + bin_adsb_packet[6] + bin_adsb_packet[7] #Da pra reduzir
               char = "" #Da pra reduzir
               char = char + cs_tbl[eval("0b"+bin_adsb_packet[8]+bin_adsb_packet[9]+bin_adsb_packet[10]+bin_adsb_packet[11]+bin_adsb_packet[12]+bin_adsb_packet[13])] #1 #Da pra reduzir
               char = char + cs_tbl[eval("0b"+bin_adsb_packet[14]+bin_adsb_packet[15]+bin_adsb_packet[16]+bin_adsb_packet[17]+bin_adsb_packet[18]+bin_adsb_packet[19])] #2 #Da pra reduzir
               char = char + cs_tbl[eval("0b"+bin_adsb_packet[20]+bin_adsb_packet[21]+bin_adsb_packet[22]+bin_adsb_packet[23]+bin_adsb_packet[24]+bin_adsb_packet[25])] #3 #Da pra reduzir
               char = char + cs_tbl[eval("0b"+bin_adsb_packet[26]+bin_adsb_packet[27]+bin_adsb_packet[28]+bin_adsb_packet[29]+bin_adsb_packet[30]+bin_adsb_packet[31])] #4 #Da pra reduzir
               char = char + cs_tbl[eval("0b"+bin_adsb_packet[32]+bin_adsb_packet[33]+bin_adsb_packet[34]+bin_adsb_packet[35]+bin_adsb_packet[36]+bin_adsb_packet[37])] #5 #Da pra reduzir
               char = char + cs_tbl[eval("0b"+bin_adsb_packet[38]+bin_adsb_packet[39]+bin_adsb_packet[40]+bin_adsb_packet[41]+bin_adsb_packet[42]+bin_adsb_packet[43])] #6 #Da pra reduzir
               char = char + cs_tbl[eval("0b"+bin_adsb_packet[44]+bin_adsb_packet[45]+bin_adsb_packet[46]+bin_adsb_packet[47]+bin_adsb_packet[48]+bin_adsb_packet[49])] #7 #Da pra reduzir
               char = char + cs_tbl[eval("0b"+bin_adsb_packet[50]+bin_adsb_packet[51]+bin_adsb_packet[52]+bin_adsb_packet[53]+bin_adsb_packet[54]+bin_adsb_packet[55])] #8 #Da pra reduzir
               UpdateAirplaneID(ICAO, char)

               #hex_adsb_packet_aircraft_type = data[:5]
               #hex_adsb_packet_aircraft_category = data[6]+data[7]+data[8]
               #formatCode = eval(bin(eval("0b" + hex_adsb_packet_aircraft_type)))
               #aircraftCategory = eval(bin(eval("0b" + hex_adsb_packet_aircraft_category)))
               #type_ = formatTypeCode[formatCode][0]
               #formatCode][1][aircraftCategory
               #print category
       
           elif TC >= 9 and TC <= 18: 
              print "Type: Airborne Position message... (Altitude, Latitude e Longitude) - Altitude Barometrica"
              hex_adsb_packet = data[8:] #Da pra reduzir
              bin_adsb_packet = c(hex_adsb_packet[0],hex_adsb_packet[1])+c(hex_adsb_packet[2],hex_adsb_packet[3])+c(hex_adsb_packet[4],hex_adsb_packet[5])+c(hex_adsb_packet[6],hex_adsb_packet[7])+c(hex_adsb_packet[8],hex_adsb_packet[9])+c(hex_adsb_packet[10],hex_adsb_packet[11])+c(hex_adsb_packet[12],hex_adsb_packet[13])
              Altitude = "0b" + bin_adsb_packet[8:][:12] #Da pra reduzir
              Latitude = eval("0b" + bin_adsb_packet[22:][:17]) #Da pra reduzir   
              Longitude =  eval("0b" + bin_adsb_packet[-17:]) #Da pra reduzir
              T = bin_adsb_packet[20:][0] #Da pra reduzir
              F = bin_adsb_packet[21:][0] #Da pra reduzir

              Altitude = Altitude[2:][:12] #Da pra reduzir
              bits = Altitude[0]+Altitude[1]+Altitude[2]+Altitude[3]+ Altitude[4]+Altitude[5]+Altitude[6]+Altitude[8]+Altitude[9]+Altitude[10]+Altitude[11] #Da pra reduzir
              oitavo_bit = Altitude[7] #Da pra reduzir
              Altitude = 25 * eval("0b"+bits) - 1000 #Da pra reduzir
              print "Altitude: " + str(Altitude)
               
              if F == '0':
                 print "Even Packet"
                 UpdateAirplanePosition_T0(ICAO, [Latitude, Longitude, Altitude])
              elif F == '1':
                 print "Odd Packet"
                 UpdateAirplanePosition_T1(ICAO, [Latitude, Longitude, Altitude])

              if VerifyAllPositionDataExists(ICAO) == True: #verifica exitencia dos dois dados e calcula rota
                   Airplanes1, Airplanes2, Airplanes3, Airplanes4 = GetPositionData(ICAO)
                   Airplanes1 = int(Airplanes1)
                   Airplanes2 = int(Airplanes2)
                   Airplanes3 = int(Airplanes3)
                   Airplanes4 = int(Airplanes4)
                   j = math.floor((59. * Airplanes1 - 60. * Airplanes2) / 131072. + 0.5)
                   rlat0 = 6. * (modulo(j, 60.) + Airplanes1 / 131072.)
                   rlat1 = rlat1 = 6.101694915254237288 * (modulo(j, 59.) + Airplanes2 / 131072.)
                   
                   if rlat0 > 270:
                       rlat0 = rlat0 - 360
                   if rlat1 > 270:
                       rlat1 = rlat1 - 360

                   NL0 = NL(rlat0)
                   NL1 = NL(rlat1)
                                                           
                   if NL0 != NL1:
                       return False

                   m = math.floor((Airplanes3 * (NL0 - 1) - Airplanes4 * NL1) / 131072. + 0.5);

                   if F == '0':
                       Latitude = rlat0
                       
                       if NL0 > 1:
                           ni = NL0
                       else:
                           ni = 1
                       
                       dlon = 360. / ni
                       rlon = dlon * (modulo(m, ni) + Airplanes3 / 131072.)
                       Longitude = rlon

                       CALLSIGN, Altitude, CLIMB, Head, VelocidadeGnd, T = getAirplaneFullLog(ICAO)
                       Data = [ICAO, CALLSIGN, Latitude, Longitude, Altitude, CLIMB, Head, VelocidadeGnd, T]

                       print "Distancia do captador: " + str(distance(Latitude, Longitude, -5.19506, -39.28307))

                       if distance(Latitude, Longitude, -5.19506, -39.28307) > 440:
                          print "Pacote Rejeitado - Distancia Muito longa."
                          return False

                       RealTimeFullAirplaneFeed(Data)
                       print "Informacao atualizada!"
                       
                   elif F == '1':
                       Latitude = rlat1
                       
                       if (NL1 - 1) > 1:
                           ni = (NL1 - 1)
                       else:
                           ni = 1
                       
                       dlon = 360. / ni
                       rlon = dlon * (modulo(m, ni) + Airplanes4 / 131072.)
                       Longitude = rlon

                       CALLSIGN, Altitude, CLIMB, Head, VelocidadeGnd, T = getAirplaneFullLog(ICAO)
                       Data = [ICAO, CALLSIGN, Latitude, Longitude, Altitude, CLIMB, Head, VelocidadeGnd, T]

                       print "Posicao do Captador - Lat: " + str(latHome) +" Lon: " + str(lonHome)
                       print "Distancia do captador: " + str(distance(Latitude, Longitude, latHome, lonHome))
                       if distance(Latitude, Longitude, latHome, lonHome) > 440:
                          print "Pacote Rejeitado - Distancia Muito longa."
                          return False
                        
                       RealTimeFullAirplaneFeed(Data)
                       print "Informacao atualizada!"
                                          
           elif TC == 19:
               print "Type: Airborne Velocity Message... (Ground Speed, Track, Vertical)"
               hex_adsb_packet = data[8:] #Da pra reduzir
               hex_adsb_packet = hex_adsb_packet[:14] #Da pra reduzir
               bin_adsb_packet = c(hex_adsb_packet[0],hex_adsb_packet[1])+c(hex_adsb_packet[2],hex_adsb_packet[3])+c(hex_adsb_packet[4],hex_adsb_packet[5])+c(hex_adsb_packet[6],hex_adsb_packet[7])+c(hex_adsb_packet[8],hex_adsb_packet[9])+c(hex_adsb_packet[10],hex_adsb_packet[11])+c(hex_adsb_packet[12],hex_adsb_packet[13]) #Da pra reduzir
               subtype = eval("0b"+bin_adsb_packet[5] + bin_adsb_packet[6] + bin_adsb_packet[7]) #Da pra reduzir

               if subtype == 0:
                  print "Velocidade: Supersonica... Corre cumpadi"
                
               if subtype == 1: # Velocidade (de Ground) nao supersonica
                  print "Velocidade: Nao-Supersonica"
                  directionBitEastWest = bin_adsb_packet[13]
                  directionBitNorthSouth = bin_adsb_packet[24]

                  numEastWest = eval("0b"+bin_adsb_packet[14]+bin_adsb_packet[15]+bin_adsb_packet[16]+bin_adsb_packet[17]+bin_adsb_packet[18]+bin_adsb_packet[19]+bin_adsb_packet[20]+bin_adsb_packet[21]+bin_adsb_packet[22]+bin_adsb_packet[23]) #Da pra reduzir
                  numNorthSouth = eval("0b"+bin_adsb_packet[25]+bin_adsb_packet[26]+bin_adsb_packet[27]+bin_adsb_packet[28]+bin_adsb_packet[29]+bin_adsb_packet[30]+bin_adsb_packet[31]+bin_adsb_packet[32]+bin_adsb_packet[33]+bin_adsb_packet[34]) #Da pra reduzir

                  gnd_spd = math.floor(math.sqrt(numEastWest * numEastWest + numNorthSouth * numNorthSouth))
            
                  if (numEastWest == 0) and (numNorthSouth == 0):
                     return False
                  else:
                      print "directionBitEastWest " + str(directionBitEastWest)
                      print "directionBitNorthSouth " + str(directionBitNorthSouth)
                      print "numEastWest " + str(numEastWest)
                      print "numNorthSouth " + str(numNorthSouth)
                      
                      directionBitEastWest = int(directionBitEastWest)
                      directionBitNorthSouth = int(directionBitNorthSouth)
                      numEastWest = int(numEastWest)
                      numNorthSouth = int(numNorthSouth)

                      trk = 0
                      if directionBitEastWest == 0 and directionBitNorthSouth == 0:
                         if numEastWest == 0:
                            trk = 0
                         else:
                            trk = 90 - 180./math.pi*math.atan(numNorthSouth / numEastWest)
                        
                      if directionBitEastWest == 0 and directionBitNorthSouth == 1:
                         if numEastWest == 0:
                            return 180
                         else:
                            trk = 90 + 180./math.pi*math.atan(numNorthSouth / numEastWest)

                      if directionBitEastWest == 1 and directionBitNorthSouth == 1:
                         if numEastWest == 0:
                            trk = 180
                         else:
                            trk = 270 - 180./math.pi*math.atan(numNorthSouth / numEastWest)

                      if directionBitEastWest == 1 and directionBitNorthSouth== 0:
                         if numEastWest == 0:
                            trk = 0
                         else:
                            trk = 270 + 180./math.pi*math.atan(numNorthSouth / numEastWest)
                            
                      if (trk - int(math.floor(trk))) < 0.5:
                        trk = int(math.floor(trk))
                      else:
                        trk = int(math.ceil(trk))
                                    
                      UpdateAirplaneAngle(ICAO, [gnd_spd, trk, 0])
                
           else:
               print 'Downlink Format: ' +str(DF) + ' Type Code:'+ str(TC) +' - Desconhecido'
               ServerReport.report('PyAdsbDecoderDataBase', '1', 'Downlink Format/type code: ' +str(DF)+"/" + str(TC) + ' - Desconhecido - '+ data)

    else:
        print 'Tamanho de invalido do pacote...'
        ServerReport.report('PyAdsbDecoderDataBase', '1', 'Tamanho de invalido do pacote - '+ data)
