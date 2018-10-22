# from twisted.internet import defer
# 
# TARGET = 10000
# 
# def largeFibonnaciNumber():
#     # create a Deferred object to return:
#     d = defer.Deferred()
# 
#     # calculate the ten thousandth Fibonnaci number
# 
#     first = 0
#     second = 1
# 
#     for i in range(TARGET - 1):
#         new = first + second
#         first = second
#         second = new
#         if i % 100 == 0:
#             print("Progress: calculating the %dth Fibonnaci number" % i)
# 
#     # give the Deferred the answer to pass to the callbacks:
#     d.callback(second)
# 
#     # return the Deferred with the answer:
#     return d
# 
# import time
# 
# timeBefore = time.time()
# 
# # call the function and get our Deferred
# d = largeFibonnaciNumber()
# 
# timeAfter = time.time()
# 
# print("Total time taken for largeFibonnaciNumber call: %0.3f seconds" % \
#       (timeAfter - timeBefore))
# 
# # add a callback to it to print the number
# 
# def printNumber(number):
#     print("The %dth Fibonacci number is %d" % (TARGET, number))
# 
# print("Adding the callback now.")
# 
# d.addCallback(printNumber)


def largeFibonnaciNumber():
    """
    Represent a long running blocking function by calculating
    the TARGETth Fibonnaci number
    """
    TARGET = 10000

    first = 0
    second = 1

    for i in range(TARGET - 1):
        new = first + second
        first = second
        second = new

    return second

from twisted.internet import threads, reactor

def fibonacciCallback(result):
    """
    Callback which manages the largeFibonnaciNumber result by
    printing it out
    """
    print("largeFibonnaciNumber result =", result)
    # make sure the reactor stops after the callback chain finishes,
    # just so that this example terminates
    reactor.stop()

def run():
    """
    Run a series of operations, deferring the largeFibonnaciNumber
    operation to a thread and performing some other operations after
    adding the callback
    """
    # get our Deferred which will be called with the largeFibonnaciNumber result
    d = threads.deferToThread(largeFibonnaciNumber)
    # add our callback to print it out
    d.addCallback(fibonacciCallback)
    print("1st line after the addition of the callback")
    print("2nd line after the addition of the callback")

if __name__ == '__main__':
    run()
    reactor.run()
