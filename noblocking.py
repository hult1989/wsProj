from twisted.internet import threads, reactor
from twisted.internet import defer
from time import time

def cc():
    print "start cc method at " , time()
    f = open('../output.txt', 'w')
    for i in xrange(20 * 1024 * 1024):
        f.write('w')
    f.close()
    print "finish cc method at " , time()
    '''
    TARGET = 1000000
    print "start cc method at " , time()
    first = 0
    second = 1
    for i in xrange(TARGET - 1):
        new = first + second
        first = second
        second = new
    print "finish cc method at " , time()
    return second
    '''

def printResult(result):
    print "result = TD;DR"
#    reactor.stop()


def run():
    d = defer.Deferred()
    d.addCallback(cc)
    d.addCallback(printResult)
    print "before callback: ", time()
    d.callback(100000)
    print "after callback: ", time()


if __name__ == "__main__":
    run()
