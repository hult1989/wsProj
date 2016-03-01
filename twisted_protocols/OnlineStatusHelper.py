import time
from twisted.internet import task, defer


class OnlineStatus(object):
    def __init__(self, imei, transport, lastvisit, buckNo):
        self.imei = imei
        self.lastvisit = lastvisit
        self.buckNo = buckNo
        self.requestDefer = None
        self.transport = transport
        self.gpsStatus = False
        self.appRequestTime = None

    def updateAppRequestTime(self):
        self.appRequestTime = time.time()

    def getAppRequestTime(self):
        return self.appRequestTime

    def switchGps(self, enable):
        if enable:
            self.transport.write(','.join(('8', self.imei, '1')) + '\r\n')
        else:
            self.transport.write(','.join(('8', self.imei, '0')) + '\r\n')
        self.requestDefer = defer.Deferred()
        return self.requestDefer

    def getDefer(self):
        if not self.requestDefer:
            self.requestDefer = defer.Deferred()
        return self.requestDefer


class OnlineStatusHelper(object):
    TASK_INTERVAL = 60
    IDLE_COUNT = 5
    def __init__(self, log):
        self.connectedSticks = {}
        self.log = log

    def getOnlineSticksNum(self):
        return len(self.connectedSticks)

    def getCurBuckNo(self):
        return  int(time.time()/self.TASK_INTERVAL) % self.IDLE_COUNT 

    def getTargetBuckNo(self):
        return (self.getCurBuckNo() + 1) % self.IDLE_COUNT

    def removeImei(self, imei):
        if imei not in self.connectedSticks:
            return 
        status = self.connectedSticks[imei]
        try:
            status.transport.loseConnection()
        except Exception as e:
            log.msg('failed to disconnect %s at %s' %(imei, str(status.transport.client)))
        del self.connectedSticks[imei]

    def getLoopingKickStart(self):
        task.LoopingCall(self.kickoutIdleConnection).start(self.TASK_INTERVAL)

    def updateOnlineStatus(self, imei, port):
        if imei not in self.connectedSticks:
            self.connectedSticks[imei] = OnlineStatus(imei, port, time.time(), self.getCurBuckNo())
            return
        status = self.connectedSticks[imei]
        if status.transport != port:
            log.msg('stick %s changed socket from %s to %s' %(imei, str(status.transport.client), str(port.client)))
            try:
                status.transport.loseConnection()
            except Exception as e:
                log.msg('failed to disconnect %s at %s' %(imei, str(status.transport.client)))
        status.transport = port
        self.connectedSticks[imei].lastvisit = time.time()
        self.connectedSticks[imei].buckNo = self.getCurBuckNo()


    def kickoutIdleConnection(self):
        tarNo  = self.getTargetBuckNo()
        cur = time.time()
        #self.log.msg('current bucket no is %s' %(self.getCurBuckNo()))
        for imei in self.connectedSticks.keys():
            if cur - self.connectedSticks[imei].lastvisit > self.IDLE_COUNT * self.TASK_INTERVAL:
                lastvisit = time.ctime(self.connectedSticks[imei].lastvisit)
                try:
                    self.removeImei(imei)
                except Exception as e:
                    self.log.msg(e)
                finally:
                    self.log.msg('kickout stick %s, its last message sent at %s' %(imei, lastvisit))

    def getStatusWebPage(self):
        title = '<title>online sticks</title>'
        head = '<h3 align="center">%s sticks connected, current no: %s</h3>' %(self.getOnlineSticksNum(), self.getCurBuckNo())
        table = '<table border="1" align="center" cellpadding=5><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>' %('ID', 'IMEI', 'GPS', 'SOCKET', 'LAST BEAT', 'BUCKET NO', 'OPERATION')
        for i, imei in enumerate(self.connectedSticks):
            table += '<tr>'
            status = self.connectedSticks[imei]
            table += '<td>%s</td>' %(i)
            table += '<td>%s</td>' %(str(status.imei))
            table += '<td>%s</td>' %(str(status.gpsStatus))
            table += '<td>%s</td>' %(str(status.transport.client))
            table += '<td>%s</td>' %(str(time.ctime(status.lastvisit)))
            table += '<td align="center">%s</td>' %(str(status.buckNo))
            table += '<td align="center"><form method="POST">'
            table += '<input type="hidden" name="imei" value="%s"/>' %(imei)
            table += '<input type="radio" name="enablegps" value="off"/>enable gps'
            table += '<input type="radio" name="disgps" value="off"/>disable gps'
            table += '<input type="radio" name="offline" value="off"/>offline'
            table += '<input type="submit" name="button" value="submit"/></form></td>'
            table += '</tr>'
        return '<!DOCTYPE html><html><head>%s</head><body>%s%s</body></html>' %(title, head, table)
       

            
        

from twisted.python import log
onlineStatusHelper = OnlineStatusHelper(log)

if __name__ == '__main__':
    from random import randint
    helper = OnlineStatusHelper(log)
    for i in range(10000, 11111):
        helper.updateOnlineStatus(randint(10000, 11111), randint(90000, 99999))
    print helper.getOnlineSticksNum()
        

