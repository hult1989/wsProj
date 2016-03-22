# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
An example of a proxy which logs all requests processed through it.

Usage:
    $ python logging-proxy.py

Then configure your web browser to use localhost:8080 as a proxy, and visit a
URL (This is not a SOCKS proxy). When browsing in this configuration, this
example will proxy connections from the browser to the server indicated by URLs
which are visited.  The client IP and the request hostname will be logged for
each request.

HTTP is supported.  HTTPS is not supported.

See also proxy.py for a simpler proxy example.
"""

from twisted.internet import reactor
from twisted.web import proxy, http
from twisted.python import log

class LoggingProxyRequest(proxy.ProxyRequest):
    def process(self):
        log.msg('---------------request---------------------------')
        log.msg("Request from %s for %s" % (self.getClientIP(), self.getAllHeaders()['host']))
        log.msg(self.args)
        log.msg(self.content.read())
        log.msg('-------------request end-------------------------')
        try:
            proxy.ProxyRequest.process(self)
        except Exception as e:
            log.msg(str(e))

class LoggingProxy(proxy.Proxy):
    requestFactory = LoggingProxyRequest

class LoggingProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return LoggingProxy()

if __name__ == '__main__':
    import sys
    log.startLogging(sys.stdout)
    reactor.listenTCP(8000, LoggingProxyFactory())
    reactor.run()
