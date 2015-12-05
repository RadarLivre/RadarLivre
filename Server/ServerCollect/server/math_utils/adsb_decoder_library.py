import math

def toHex(x):
    return hex(eval("0x" + x))

def toBin(x):
    return bin(eval("0b" + x))

def full_bit_zero(data):
    data = data[2:]
    falta = 8 - len(data)
    for x in range(0, falta):
        data= '0' + data
    return data

def distance(lat, lon, lat1, lon1):
    return (6371 * math.acos(math.sin(lat * math.pi / 180.) * math.sin(lat1 * math.pi / 180.)
          + math.cos(lat * math.pi / 180.) * math.cos(lat1 * math.pi / 180.) * math.cos((lon - lon1) * math.pi / 180.)))

def c(d1, d2):
    return full_bit_zero(bin(eval(toHex(d1+d2))))

def modulo(x, y):
    r = x - y * math.floor(x / y)
    return r

def NL(lat):
	if math.fabs(lat) < 10.47047130:
		return 59
	elif math.fabs(lat) < 14.82817437:
		return 58
	elif math.fabs(lat) < 18.18626357:
		return 57
	elif math.fabs(lat) < 21.02939493:
		return 56
	elif math.fabs(lat) < 23.54504487:
		return 55
	elif math.fabs(lat) < 25.82924707:
		return 54
	elif math.fabs(lat) < 27.93898710:
		return 53
	elif math.fabs(lat) < 29.91135686:
		return 52
	elif math.fabs(lat) < 31.77209708:
		return 51
	elif math.fabs(lat) < 33.53993436:
		return 50
	elif math.fabs(lat) < 35.22899598:
		return 49
	elif math.fabs(lat) < 36.85025108:
		return 48
	elif math.fabs(lat) < 38.41241892:
		return 47
	elif math.fabs(lat) < 39.92256684:
		return 46
	elif math.fabs(lat) < 41.38651832:
		return 45
	elif math.fabs(lat) < 42.80914012:
		return 44
	elif math.fabs(lat) < 44.19454951:
		return 43
	elif math.fabs(lat) < 45.54626723:
		return 42
	elif math.fabs(lat) < 46.86733252:
		return 41
	elif math.fabs(lat) < 48.16039128:
		return 40
	elif math.fabs(lat) < 49.42776439:
		return 39
	elif math.fabs(lat) < 50.67150166:
		return 38
	elif math.fabs(lat) < 51.89342469:
		return 37
	elif math.fabs(lat) < 53.09516153:
		return 36
	elif math.fabs(lat) < 54.27817472:
		return 35
	elif math.fabs(lat) < 55.44378444:
		return 34
	elif math.fabs(lat) < 56.59318756:
		return 33
	elif math.fabs(lat) < 57.72747354:
		return 32
	elif math.fabs(lat) < 58.84763776:
		return 31
	elif math.fabs(lat) < 59.95459277:
		return 30
	elif math.fabs(lat) < 61.04917774:
		return 29
	elif math.fabs(lat) < 62.13216659:
		return 28
	elif math.fabs(lat) < 63.20427479:
		return 27
	elif math.fabs(lat) < 64.26616523:
		return 26
	elif math.fabs(lat) < 65.31845310:
		return 25
	elif math.fabs(lat) < 66.36171008:
		return 24
	elif math.fabs(lat) < 67.39646774:
		return 23
	elif math.fabs(lat) < 68.42322022:
		return 22
	elif math.fabs(lat) < 69.44242631:
		return 21
	elif math.fabs(lat) < 70.45451075:
		return 20
	elif math.fabs(lat) < 71.45986473:
		return 19
	elif math.fabs(lat) < 72.45884545:
		return 18
	elif math.fabs(lat) < 73.45177442:
		return 17
	elif math.fabs(lat) < 74.43893416:
		return 16
	elif math.fabs(lat) < 75.42056257:
		return 15
	elif math.fabs(lat) < 76.39684391:
		return 14
	elif math.fabs(lat) < 77.36789461:
		return 13
	elif math.fabs(lat) < 78.33374083:
		return 12
	elif math.fabs(lat) < 79.29428225:
		return 11
	elif math.fabs(lat) < 80.24923213:
		return 10
	elif math.fabs(lat) < 81.19801349:
		return 9
	elif math.fabs(lat) < 82.13956981:
		return 8
	elif math.fabs(lat) < 83.07199445:
		return 7
	elif math.fabs(lat) < 83.99173563:
		return 6
	elif math.fabs(lat) < 84.89166191:
		return 5
	elif math.fabs(lat) < 85.75541621:
		return 4
	elif math.fabs(lat) < 86.53536998:
		return 3
	elif math.fabs(lat) < 87.00000000:
		return 2
	else:
		return 1
