from twisted.python import log
from json import dumps


def resultValue(n):
    return dumps({'result': str(n)})

def onError(error):
    log.msg(error)


