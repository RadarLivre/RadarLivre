def b112_crc(adsb_payload_11_bytes):
    poly = 0xFFFA0480
    data = \
        (adsb_payload_11_bytes[0] << 24) | \
        (adsb_payload_11_bytes[1] << 16) | \
        (adsb_payload_11_bytes[2] <<  8) | \
        (adsb_payload_11_bytes[3] <<  0)
    data1 = \
        (adsb_payload_11_bytes[4] << 24) | \
        (adsb_payload_11_bytes[5] << 16) | \
        (adsb_payload_11_bytes[6] <<  8) | \
        (adsb_payload_11_bytes[7] <<  0)
    data2 = \
        (adsb_payload_11_bytes[8] << 24) | \
        (adsb_payload_11_bytes[9] << 16) | \
        (adsb_payload_11_bytes[10] <<  8)
    result = 0x00000000
    for _ in range(0, 88):
        if (data & 0x80000000) != 0:
            data = data ^ poly
        data = data << 1
        if (data1 & 0x80000000) != 0:
            data = data | 1
        data1 = data1 << 1
        if (data2 & 0x80000000) != 0:
            data1 = data1 | 1
        data2 = data2 << 1
    result = result ^ data
    return result >> 8

def b56_crc(adsb_payload_4_bytes):
    poly = 0xFFFA0480
    data = \
        (adsb_payload_4_bytes[0] << 24) | \
        (adsb_payload_4_bytes[1] << 16) | \
        (adsb_payload_4_bytes[2] <<  8) | \
        (adsb_payload_4_bytes[3] <<  0)
    result = 0x00000000
    for _ in range(0, 32):
        if (data & 0x80000000) != 0:
            data = data ^ poly
        data = data << 1
    result = result ^ data
    return result >> 8

def parity56(frame):
   '''
        type  icao       alt   CRC
        5F   E4,82,C6   C0,66  CF
   '''
   adsb_msg = [
               eval("0x"+frame[0]+frame[1]),   eval("0x"+frame[2]+frame[3]),   eval("0x"+frame[4]+frame[5]), 
               eval("0x"+frame[6]+frame[7]),   eval("0x"+frame[8]+frame[9]+frame[10]+frame[11]+frame[12]+frame[13])
              ]
   
   #[0x5d, 0xa5, 0xdb, 0x4e, 0xf5f740]

   res = b56_crc(adsb_msg[0:6])
   ver = adsb_msg[6]
   if res != ver:
     return False
   else:
     return True
    
def parity112(frame):
    
   adsb_msg = [
               eval("0x"+frame[0]+frame[1]),   eval("0x"+frame[2]+frame[3]),   eval("0x"+frame[4]+frame[5]), 
               eval("0x"+frame[6]+frame[7]),   eval("0x"+frame[8]+frame[9]),   eval("0x"+frame[10]+frame[11]),
               eval("0x"+frame[12]+frame[13]), eval("0x"+frame[14]+frame[15]), eval("0x"+frame[16]+frame[17]),
               eval("0x"+frame[18]+frame[19]), eval("0x"+frame[20]+frame[21]), eval("0x"+frame[22]+frame[23]+frame[24]+frame[25]+frame[26]+frame[27])
              ]

   res = b112_crc(adsb_msg[0:11])
   ver = adsb_msg[11]
   if res != ver:
     return False
   else:
     return True




