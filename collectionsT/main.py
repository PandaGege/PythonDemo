# coding: utf-8
# ----------------------------------------------
# author            : regan
# email             : x-regan@qq.com
# create at         : 2018-05-27 16:06
# last modify       : 2018-05-27 16:06
# ----------------------------------------------

import random
from collections import Counter, deque, defaultdict, namedtuple


def counter():
    # Counter([iterable-or-mapping])
    # or Counter(dog=12, cat=22)
    c = Counter([chr(random.randint(1, 129)) for i in range(100)])
    # count值最大的10个
    print c.most_common(10)

    # c['A'] = 0，并不会删除元素，用del
    del c['D']

    # elements返回元素的迭代器，如果值小于1将会被忽略
    print list(c.elements())

    # subtract(iterable-or-mapping]) 减
    c1 = Counter(a=12, b=10, c=-2)
    c2 = Counter(a=-12, b=3, c=5, d=2)
    c1.subtract(c2)
    print c1

    #update(iterable-or-mapping]) 加，用法类似于subtract


def func_deque():
    """
        collections.deque([iterable[, maxlen]])
        双向队列。线程安全，内存优化，从任意一端pop or append复杂度为o(1)
        如果初始化时指定maxlen那么它将成为定长队列，如果append时超过maxlen，
        将会从另一侧丢弃元素

        functions:
            append(x)
            appendleft(x)
            clear()
            count(x)
            extend(iterable)
            extendleft(iterable)
            pop()
            popleft()
            remove(value)
                remove 从左开始移除第一个值等于value的元素
            reverse()
            rotate(n=1)
                向右旋转n步，如果n是负数, 则向左旋转
            maxlen
    """
    dq = deque((1,2,41,41,21,41,4))
    dq.remove(41)
    print dq
    dq.rotate(3)
    print dq


def defaultdict_demo():
    '''
        class collections.defaultdict([default_factory[, ...]])
        value为空的以default_factory初始化
        其它用法和dict一致
    '''
    s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    d = defaultdict(list)
    for k,v in s:
        d[k].append(v)
    for k, v in d.items():
        print k, v


def namedtuple_demo():
    '''
        Point = namedtuple('Point', ['x', 'y'], verbose=True)
        verbose=True会打印出Point的类定义：

            class Point(tuple):
                'Point(x, y)'

                __slots__ = ()

                _fields = ('x', 'y')

                def __new__(_cls, x, y):
                    'Create new instance of Point(x, y)'
                    return _tuple.__new__(_cls, (x, y))

                @classmethod
                def _make(cls, iterable, new=tuple.__new__, len=len):
                    'Make a new Point object from a sequence or iterable'
                    result = new(cls, iterable)
                    if len(result) != 2:
                        raise TypeError('Expected 2 arguments, got %d' % len(result))
                    return result

                def __repr__(self):
                    'Return a nicely formatted representation string'
                    return 'Point(x=%r, y=%r)' % self

                def _asdict(self):
                    'Return a new OrderedDict which maps field names to their values'
                    return OrderedDict(zip(self._fields, self))

                def _replace(_self, **kwds):
                    'Return a new Point object replacing specified fields with new values'
                    result = _self._make(map(kwds.pop, ('x', 'y'), _self))
                    if kwds:
                        raise ValueError('Got unexpected field names: %r' % kwds.keys())
                    return result

                def __getnewargs__(self):
                    'Return self as a plain tuple.  Used by copy and pickle.'
                    return tuple(self)

                __dict__ = _property(_asdict)

                def __getstate__(self):
                    'Exclude the OrderedDict from pickling'
                    pass

                x = _property(_itemgetter(0), doc='Alias for field number 0')

                y = _property(_itemgetter(1), doc='Alias for field number 1')

        1, __slots__ 禁止了绑定实例方法，可以限制内存占用
        2, 元素访问是通过 描述符实现的.
    '''
    Point = namedtuple('Point', ['x', 'y'], verbose=True)
    p = Point(12,13)
    x,y = p
    print x, y
    print p
    p.x = 12 # error, tuple can`t be set





if __name__ == '__main__':
    # counter()
    # func_deque()
    # defaultdict_demo()
    # namedtuple_demo()
