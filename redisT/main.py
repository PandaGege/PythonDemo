# -*- coding:utf-8 -*-

import redis
import random

def conn_redis():
    return redis.StrictRedis(host="192.168.94.168", port=18300, db=0)


def main():
    rconn = conn_redis()
    keys = rconn.keys()

    ip = random.choice(keys)
    port = rconn.hget(ip, 'port')

    rconn.delete(ip)
    #rconn.hmset(key, dict)

if __name__ == "__main__":
    main()
