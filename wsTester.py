from twisted.test import proto_helpers
from twisted.trial import unittest

from wsServer import WsServerFactory

class WsServerTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = WsServerFactory()
        self.proto = self.factory.buildProtocol(('localhost', 0))
        self.transport = proto_helpers.StringTransport()
        self.ptoro.makeConnection(self.transport)

    def testLocation(self):
        self.assertEqual(self.transport.value(), 'Result:4,1')
