# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from elasticsearch import helpers

from time import time

from proxies.cache_server.config import es
from proxies.cache_server.config import logger

def add(proxies, index):
    actions = [
        {   
            "_index": index,
            "_type" : "proxy", 
            "_id" : proxy['ip address'] + ':' + proxy['port'], 
            "_source": proxy,
            "op_type": "create"
        }
        for proxy in proxies
    ]
    if proxies:
        print('# of working proxies: ', len(proxies))
        try:
            tic = time()
            helpers.bulk(es, actions)
            tac = time()
            print('Time taken to add to index: ', tac - tic)
        except Exception as e:
            template = 'An exception of type {0} occurred.\nArguments: {1!r}'
            message = template.format(type(e).__name__, e.args)
            logger.error(message)