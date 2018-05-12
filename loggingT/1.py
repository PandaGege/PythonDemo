# -*- coding:utf-8 -*-



import time
import logging
from random import choice


'''
模块级别的方法：
    logging.getLogger([name])
    logging.getLoggerClass()
    logging.debug(msg[, *args[, **kwargs]])
        用root logger处理日志消息
        同logging.info, logging.error....
    logging.disable(lvl) 禁用日志等级
    logging.addLevelName(lvl, levelName) 添加自定义日志等级与name
    logging.getLevelName(lvl)
    logging.makeLogRecord(attrdict)
    logging.basicConfig([**kwargs])
    logging.shutdown()  flush & close 所以handler, 调用后不能再用logging
    logging.setLoggerClass(klass)
'''

#从模块级别禁止日志等级
#logging.disable(logging.ERROR)

'''
logging.basicConfig([**kwargs])
    filename
    filemode
    format
    datefmt
    level
    stream
'''
logging.basicConfig(format='%(asctime)-15s %(name)-5s %(levelname)-8s '\
    '%(message)s', level=10)


'''
1,建议以__name__作为logger的name
2,foo, foo.bar, foo.bar.baz分别是爷爷，父亲，儿子
3，多次getLogger，相同name返回相同对象
4, 不写name时，为root logger
'''
logger = logging.getLogger('top')


def init_logger():
    '''
    1,propagate 默认为True
    2,当为True时，日志事件除了该logger会处理外，还会传递给所有祖先的handler
    如果该logger和祖先logger都绑定了handler,日志有可能会处理两次
    3,通用的场景是只由root logger绑定handler
    '''
    logger.propagate = True

    '''
    1, 比setlevel等级低的日志将被忽略
    2, level默认为NOTSET，root logger默认为WARNING
    3, 日志事件向祖先传递时，祖先的level实际作用
    4,  CRITICAL    50
        ERROR   40
        WARNING 30
        INFO    20
        DEBUG   10
        NOTSET  0
    '''
    logger.setLevel(logging.INFO)

    '''
    检查是否为有效日志等级
    先检查logging.disable(lvl)禁止的等级
    再根据Logger.getEffectiveLevel的结果决定
    '''
    print logger.isEnabledFor(logging.ERROR)
    print logger.isEnabledFor(logging.DEBUG)

    '''
    1,如果logger用setLevel设置的level比NOTSET高，则返回该值
    2,否则，由祖先的level决定。确实如此，why?
    '''
    print logger.getEffectiveLevel()

    '''
    logging.getLogger('abc').getChild('def.ghi')
    等效于logging.getLogger('abc.def.ghi')
    '''
    child = logger.getChild('son')
    print child.name # top.son
    
    '''
    1, Logger.debug(msg, *args, **kwargs)
    方法debug,error,info,warning,critical用法一样
    kwargs中的exc_info, extra会被检查

    2, Logger.log(lvl, msg, *args, **kwargs)需要指定level
    3, Logger.exception(msg, *args, **kwargs)
       以ERROR等级记录日志，kwargs中的exc_info不起作用,异常信息会添加到日志中
       只能用在错误处理的地方,比如except:  追加的信息类似traceback.format_exc()
    '''
    # FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    # logging.basicConfig(format=FORMAT)
    # d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
    # logger.error('djsaodaoj', extra=d)

    '''
    Logger.addFilter(filter)
    Logger.removeFilter(filter)
    Logger.filter(record)
    Logger.addHandler(hdlr)
    Logger.removeHandler(hdlr)
    Logger.findCaller()
    Logger.handle(record)
    Logger.makeRecord(name, lvl, fn, lno, msg, args, exc_info,\ 
        "func=None, extra=None)
    '''

    logfilter = init_filter()
    logger.addFilter(logfilter)

    handler = init_handlers()
    logger.addHandler(handler)
    for i in xrange(1000):
        logger.info('info')
        logger.error('error')
        time.sleep(10)


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    Rather than use actual contextual information, we just use random
    data in this demo.
    """

    USERS = ['jim', 'fred', 'sheila']
    IPS = ['123.231.231.123', '127.0.0.1', '192.168.0.1']

    def filter(self, record):

        record.ip = choice(ContextFilter.IPS)
        record.user = choice(ContextFilter.USERS)
        return True


def init_filter():
    f = ContextFilter()
    return f


def init_handlers():
    '''
    Handlers中常用的方法有:
        Handler.setLevel(level)
        Handler.setFormatter(fmt)
        Handler.addFilter(filter)
        Handler.removeFilter(filter)
    通常不直接使用Handler，而是它的子类:
        module: logging包括：
            StreamHandler
            FileHandler
            NullHandler
        module: logging.handlers包括：
            WatchedFileHandler
            RotatingFileHandler
            TimedRotatingFileHandler
            SocketHandler
            DatagramHandler
            SysLogHandler
            NTEventLogHandler
            SMTPHandler
            MemoryHandler
            HTTPHandler
    '''

    # '''
    # 常用之一：RotatingFileHandler
    # class logging.handlers.RotatingFileHandler(filename, mode='a',\
    #     maxBytes=0, backupCount=0, encoding=None, delay=0)
    # '''
    # from logging.handlers import RotatingFileHandler
    # handler = RotatingFileHandler('app.log', mode='a',\
    #    maxBytes=1024 * 1024 * 500, backupCount=20)
    # #比 INFO level低的日志消息将被忽略
    # handler.setLevel(logging.INFO)

    # formatter = logging.Formatter("%(asctime)s %(threadName)s "\
    #     "%(levelname)s: %(message)s")
    # handler.setFormatter(formatter)
    # return handler


    '''
    常用之二：TimedRotatingFileHandler
    class logging.handlers.TimedRotatingFileHandler(filename, when='h',\
      interval=1, backupCount=0, encoding=None, delay=False, utc=False)
    when:
        'S' Seconds
        'M' Minutes
        'H' Hours
        'D' Days
        'W0'-'W6'   Weekday (0=Monday)
        'midnight'  Roll over at midnight, 常用，以日期按天分割
    interval:
        和when一起作用

    '''
    from logging.handlers import TimedRotatingFileHandler
    handler = TimedRotatingFileHandler('web.log', when='M', interval=2)

    formatter = logging.Formatter("%(asctime)s %(threadName)s "\
        "%(levelname)s: %(message)s IP: %(ip)-15s User: %(user)-8s")
    handler.setFormatter(formatter)
    return handler


def init_formatter():
    '''
        https://docs.python.org/2/library/logging.html#logging.LogRecord
    '''



def main():
    init_logger()

if __name__ == '__main__':
    main()
