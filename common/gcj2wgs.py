from math import pi, sin, sqrt, cos

a = 6378245.0
ee = 0.00669342162296594323

def transform(wgLat, wgLon):
    if outOfChina(wgLat, wgLon):
        return wgLon, wgLat

    dLat = transformLat(wgLon - 105.0, wgLat - 35.0)
    dLon = transformLon(wgLon - 105.0, wgLat - 35.0)
    radLat = wgLat / 180.0 * pi
    magic = sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = sqrt(magic)
    dLat = (dLat * 180.0) / (a * (1-ee) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * cos(radLat) * pi)
    mgLat = wgLat + dLat
    mgLon = wgLon + dLon
    return mgLon, mgLat

def outOfChina(lat, lon):
    if lon < 72.004 or lon > 137.8347 or lat < 0.8293 or lat > 55.8271:
        return True
    return False

def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
    ret += (20 * sin(6.0*x*pi) + 20 * sin(2.0*x*pi)) * 2.0 / 3.0
    ret += (20 * sin(y * pi) + 40.0 * sin(y/3.0 * pi)) * 2 / 3
    ret += (160 * sin(y /12 * pi) + 320 * sin(y * pi / 30)) * 2 / 3
    return ret

def transformLon(x, y):
    ret = 300 + x + 2 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
    ret += (20 * sin(6 * x * pi) + 20 * sin(2 * x * pi) ) * 2 / 3.0
    ret += 20 * sin(x*pi) + 40 * sin( x / 3.0 * pi) * 2 / 3
    ret += (150 * sin(x/12.0 * pi) + 300 * sin(x / 30 * pi)) * 2 / 3.0
    return ret
    


if __name__ == '__main__':
    import sys
    print 'wsg84 ', (transform(float(sys.argv[2]), float(sys.argv[1])))
    print 'gcg02 ', (float(sys.argv[1]), float(sys.argv[2]))
