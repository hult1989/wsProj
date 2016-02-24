import time
from twisted.internet import task
class OnlineStatusHelper(object):
    TASK_INTERVAL = 60
    IDLE_COUNT = 6
    class OnlineStatus(object):
        def __init__(self, imei, transport, lastvisit, buckNo):
            self.imei = imei
            self.socket = transport.client
            self.lastvisit = lastvisit
            self.buckNo = buckNo

    def __init__(self, log):
        self.connectedSticks = {}
        self.log = log

    def getOnlineSticksNum(self):
        return len(self.connectedSticks)

    def getCurBuckNo(self):
        return  int(time.time()/self.TASK_INTERVAL) % self.IDLE_COUNT 

    def getTargetBuckNo(self):
        return (self.getCurBuckNo() + 1) % self.IDLE_COUNT

    def removePort(self, port):
        port.loseConnection()
        if port in self.connectedSticks:
            del self.connectedSticks[port]
            return True
        return False

    def getLoopingKickStart(self):
        task.LoopingCall(self.kickoutIdleConnection).start(self.TASK_INTERVAL)



    def updateOnlineStatus(self, port, imei):
        if port not in self.connectedSticks:
            self.connectedSticks[port] = self.OnlineStatus(imei, port, time.ctime(), self.getCurBuckNo())
            return
        if self.connectedSticks[port].imei != imei:
            self.log.msg('transport %s conflicts, before imei is %s, current imei is %s' %(port.client, self.connectedSticks[port], imei))
            self.connectedSticks[port].imei = imei
        self.connectedSticks[port].lastvisit = time.ctime()
        self.connectedSticks[port].buckNo = self.getCurBuckNo()


    def kickoutIdleConnection(self):
        tarNo  = self.getTargetBuckNo()
        self.log.msg('current bucket no is %s' %(self.getCurBuckNo()))
        for port in self.connectedSticks:
            self.log.msg('online sticks %s' %(str(vars(self.connectedSticks[port]))))
        for port in self.connectedSticks.keys():
            if self.connectedSticks[port].buckNo == tarNo:
                try:
                    self.removePort(port)
                except Exception as e:
                    self.log.msg(e)
                finally:
                    self.log.msg('kickout connection %s' %(str(port.client)))

    def getStatusWebPage(self):
        title = '<title>online sticks</title>'
        head = '<h3 align="center">%s sticks connected, current no: %s</h3>' %(self.getOnlineSticksNum(), self.getCurBuckNo())
        table = '<table border="1" align="center" cellpadding=5><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>' %('ID', 'IMEI', 'SOCKET', 'LAST BEAT', 'BUCKET NO', 'FORCED OFFLINE')
        for i, port in enumerate(self.connectedSticks):
            table += '<tr>'
            status = self.connectedSticks[port]
            table += '<td>%s</td>' %(i)
            table += '<td>%s</td>' %(str(status.imei))
            table += '<td>%s</td>' %(str(status.socket))
            table += '<td>%s</td>' %(str(status.lastvisit))
            table += '<td align="center">%s</td>' %(str(status.buckNo))
            table += '<td align="center"><form method="POST"><input type="submit" name="button" value="%s" /></form></td>' %(self.connectedSticks[port].imei)
            table += '</tr>'
        return '<!DOCTYPE html><html><head>%s</head><body>%s%s</body></html>' %(title, head, table)
       

            
        


if __name__ == '__main__':
    from random import randint
    from twisted.python import log
    helper = OnlineStatusHelper(log)
    for i in range(10000, 11111):
        helper.updateOnlineStatus(randint(10000, 11111), randint(90000, 99999))
    print helper.getOnlineSticksNum()
        

