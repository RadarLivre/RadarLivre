from server.decoder.adsb_decoder import ADSBDataDecoder

print "Lendo o Log"

f = file("adsblog.log", "r")
for linha in f:
    linha = linha.replace('\n', '')
    print len(linha)
    ADSBDataDecoder(str(linha))

