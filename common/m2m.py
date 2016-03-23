# -*- coding: utf-8 -*-

import urllib, urllib2
import json

proxyConfig = 'http://qqcloud:8000'
opener = urllib2.build_opener(urllib2.ProxyHandler({'http': proxyConfig}))
urllib2.install_opener(opener)

body = '{"sign":"B9835164AACCA855FC2454A31D9DD735","requesttime":"2016032207240424400000000","servicecode":"cz015","partnercode":"100861343","key":"14766805732"}'
address = 'http://218.207.148.170:89/V2/siminfoquery.ashx'


body = json.dumps(eval(body))
print body
request = urllib2.Request(address, body)
resp = urllib2.urlopen(request)
print resp.read()

