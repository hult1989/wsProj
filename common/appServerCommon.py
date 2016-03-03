# -*- coding:utf-8 -*-
from twisted.python import log
from json import dumps
from appException import AppException


def resultValue(n):
    return dumps({'result': str(n)})

def onError(error, request):
    if isinstance(error.value, AppException):
        request.write(resultValue(error.value.errCode))
    else:
        log.msg(error)
    request.finish()

def onSuccess(result, request):
    request.write(resultValue(1))
    request.finish()


def checkValid(payload):
    if len(payload) == 0:
        return False
    if type(payload) is str:
        return True
    if type(payload) is list or tuple:
        for p in payload:
            if checkValid(p) == False:
                return False
    if type(payload) is dict:
        for p in payload.values():
            if checkValid(p) == False:
                return False
    return True        


class appRequest:
    def __init__(self, requestDict):
        self.request = requestDict
        self.isValid = checkValid(self.request)

if __name__ == '__main__':
    d = {'name': 'alice', 'age': '23', 'location': {'con': 'd', 'name': ['a', {'d': '2'}]}}
    r = appRequest(d)
    print vars(r)
