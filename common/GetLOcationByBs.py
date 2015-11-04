import urllib2, urllib

request = urllib2.Request('http://apilocate.amap.com/position')
#secret key of gaode map service
AMAP_SERVICE_KEY = '56f2c85f19dbfae6269363d64d688173'


def getLocationByBsinfo(imei, imsi, bts):
    paramsDict = dict()
    paramsDict['accesstype'] = '0'
    paramsDict['key'] = AMAP_SERVICE_KEY
    paramsDict['output'] = 'json'
    paramsDict['imei'] = imei
    paramsDict['imsi'] = imsi
    paramsDict['bts'] = '460,00,9763,3593,-65'
    params = urllib.urlencode(paramsDict)
    request.add_data(params)
    locations = urllib2.urlopen(request).read()
    return locations

print getLocationByBsinfo(111,222,0)
