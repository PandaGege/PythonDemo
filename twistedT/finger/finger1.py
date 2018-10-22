# coding: utf-8
# ----------------------------------------------
# author            : regan
# email             : x-regan@qq.com
# create at         : 2018-06-12 16:47
# last modify       : 2018-06-12 16:47
# ----------------------------------------------

import os
import sys
from twisted.internet import reactor, protocol, endpoints, defer, utils
from twisted.protocols import basic


class FingerProtocol(basic.LineReceiver):
    def connectionMade(self):
        # self.transport.loseConnection()
        sys.stderr.write('connect..'+os.linesep)

    def lineReceived(self, user):
        # self.transport.write(b'No such user\r\n')
        # self.transport.loseConnection()
        d = self.factory.getUser(user)

        def onError(err):
            # return 'Internal error in server'
            self.transport.write(b'Internal error in server, dsd'+ b'\r\n')
            self.transport.loseConnection()
        d.addErrback(onError)

        def writeResponse(message):
            self.transport.write(message + b'\r\n')
            self.transport.loseConnection()
        d.addCallback(writeResponse)


class FingerFactory(protocol.ServerFactory):
    protocol = FingerProtocol

    def __init__(self, users):
        self.users = users

    def do_get(self, user):
        if user in self.users:
            return self.users[user]
        else:
            raise ValueError('internal error')


    def getUser(self, user):
        # return defer.succeed(self.do_get(user))
        return utils.getProcessOutput(b'finger', [user])
    

fingerEndpoint = endpoints.serverFromString(reactor, 'tcp:1079')
fingerEndpoint.listen(FingerFactory({b'regan': b'i`m regan'}))
reactor.run()
