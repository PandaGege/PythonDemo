# coding: utf-8
# ----------------------------------------------
# author            : regan
# email             : x-regan@qq.com
# create at         : 2018-06-29 10:28
# last modify       : 2018-06-29 10:28
# ----------------------------------------------

from twisted.internet import reactor, defer
from twisted.python.failure import Failure
from twisted.python import log

# class Getter:
#     def gotResults(self, x):
#         """
#         The Deferred mechanism provides a mechanism to signal error
#         conditions.  In this case, odd numbers are bad.
# 
#         This function demonstrates a more complex way of starting
#         the callback chain by checking for expected results and
#         choosing whether to fire the callback or errback chain
#         """
#         if self.d is None:
#             print("Nowhere to put results")
#             return
# 
#         d = self.d
#         self.d = None
#         if x % 2 == 0:
#             d.callback(x*3)
#         else:
#             d.errback(ValueError("You used an odd number!"))
# 
#     def _toHTML(self, r):
#         """
#         This function converts r to HTML.
# 
#         It is added to the callback chain by getDummyData in
#         order to demonstrate how a callback passes its own result
#         to the next callback
#         """
#         return "Result: %s" % r
# 
#     def getDummyData(self, x):
#         """
#         The Deferred mechanism allows for chained callbacks.
#         In this example, the output of gotResults is first
#         passed through _toHTML on its way to printData.
# 
#         Again this function is a dummy, simulating a delayed result
#         using callLater, rather than using a real asynchronous
#         setup.
#         """
#         self.d = defer.Deferred()
#         # simulate a delayed result by asking the reactor to schedule
#         # gotResults in 2 seconds time
#         reactor.callLater(2, self.gotResults, x)
#         self.d.addCallback(self._toHTML)
#         return self.d
# 
# def cbPrintData(result):
#     print(result)
# 
# def ebPrintError(failure):
#     import sys
#     sys.stderr.write(str(failure))
# 
# # this series of callbacks and errbacks will print an error message
# g = Getter()
# d = g.getDummyData(3)
# d.addCallback(cbPrintData)
# d.addErrback(ebPrintError)
# 
# # this series of callbacks and errbacks will print "Result: 12"
# g = Getter()
# d = g.getDummyData(4)
# d.addCallback(cbPrintData)
# d.addErrback(ebPrintError)
# 
# reactor.callLater(4, reactor.stop)
# reactor.run()


d = defer.Deferred()
reactor.callLater(2, d.callback, 4)
# reactor.callLater(2, d.errback, ValueError('1234'))

def callback_a(result):
    return "callback_a: %s"%result

def callback_b(result):
    raise ValueError('aaa')
    return "callback_b: %s"%result

def callback_c(result):
    return "callback_c: %s"%result


def callback_print(result):
    # raise ValueError('cause a error')
    # return Failure('a error')
    print result


def errback_a(failure):
    import sys
    failure.trap(FloatingPointError)
    sys.stderr.write(str(failure))
    return 'a error'

def errback_b(failure):
    import sys
    failure.trap(ValueError)
    sys.stderr.write(str(failure))
    return 'a error'

d.addCallback(callback_a)
# d.addErrback(errback_a)
d.addCallback(callback_b)
# d.addErrback(errback_b)
d.addCallback(callback_c)
d.addCallback(callback_print)
d.addErrback(log.err)

reactor.callLater(3, reactor.stop)
reactor.run()
