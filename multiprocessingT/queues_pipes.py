# coding: utf-8
# ----------------------------------------------
# author            : regan
# email             : x-regan@qq.com
# create at         : 2018-05-20 15:32
# last modify       : 2018-05-21 20:55
# ----------------------------------------------


import os
from Queue import Empty
from multiprocessing import Process, Queue, Pipe


def f(conn, q, op='recv'):
    if op == 'recv':
        while True:
            i = conn.recv()
            if i > 90:
                break
            q.put(i**2)
    if op == 'send':
        for i in xrange(100):
            conn.send(i)


if __name__ == '__main__':
    q = Queue()
    #parent_conn, child_conn一个用于发送
    parent_conn, child_conn = Pipe()

    parent_conn.send(1)
    p1 = Process(target=f, args=(parent_conn, q, 'recv'))
    p1.start()

    p2 = Process(target=f, args=(child_conn, q, 'send'))
    p2.start()

    while True:
        try:
            i = q.get(block=True, timeout=3)
            print i
        except Empty:
            print 'empty'
            break

    p1.join()
    p2.join()
