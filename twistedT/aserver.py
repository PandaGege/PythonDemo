# coding: utf-8
# ----------------------------------------------
# author            : regan
# email             : x-regan@qq.com
# create at         : 2018-06-11 18:08
# last modify       : 2018-06-11 18:08
# ----------------------------------------------

import sys

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class Chat(LineReceiver):
    def __init__(self, addr):
        self.addr = addr
        sys.stderr.write(str(addr))
        # self.cli_method, self.cli_host, self.cli_port = addr

    def connectionMode(self):
        self.sendLine('What`s your name')

    def connectionLost(self, reason):
        sys.stderr.write('close a connection')

    def lineReceived(self, line):
        self.sendLine('i have got: {}'.format(line))


class AFactory(Factory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return Chat(addr)


reactor.listenTCP(1234, AFactory())
reactor.run()
