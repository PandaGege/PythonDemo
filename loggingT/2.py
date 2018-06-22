# coding: utf-8
# ----------------------------------------------
# author            : regan
# email             : x-regan@qq.com
# create at         : 2018-06-22 19:34
# last modify       : 2018-06-22 19:34
# ----------------------------------------------


import logging
import logging.config
from process import func


logging.config.fileConfig('./logging.conf')
logger = logging.getLogger('server')

logging.info('root logger info log')


def main():
    # this will no print, server logger`s level is INFO
    logger.debug('server logger debug log')
    logger.info('server logger info log')
    logger.warning('server logger warning log')
    logger.error('server logger error log')
    func()


if __name__ == '__main__':
    main()
