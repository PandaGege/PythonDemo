# coding: utf-8
# ----------------------------------------------
# author            : regan
# email             : x-regan@qq.com
# create at         : 2018-06-11 16:45
# last modify       : 2018-06-11 16:45
# ----------------------------------------------


from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.internet.protocol import Protocol


class QOTD(Protocol):
    def connectionMade(self):
        self.transport.write("An apple a day keeps the doctor away\r\n")
        # self.transport.loseConnection()


class QOTDFactory(Factory):
    def buildProtocol(self, addr):
        return QOTD()


# 8007 is the port you want to run under. Choose something >1024
endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(QOTDFactory())
reactor.run()


# from twisted.internet.protocol import Factory, Protocol
# from twisted.internet.endpoints import TCP4ServerEndpoint
# from twisted.internet import reactor
# 
# class QOTD(Protocol):
# 
#     def connectionMade(self):
#         # self.factory was set by the factory's default buildProtocol:
#         self.transport.write(self.factory.quote + '\r\n')
#         self.transport.loseConnection()
# 
# 
# class QOTDFactory(Factory):
# 
#     # This will be used by the default buildProtocol to create new protocols:
#     protocol = QOTD
# 
#     def __init__(self, quote=None):
#         self.quote = quote or 'An apple a day keeps the doctor away'
# 
# endpoint = TCP4ServerEndpoint(reactor, 8007)
# endpoint.listen(QOTDFactory("configurable quote"))
# reactor.run()
