# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from random import choice

from proxies.cache_server.config import es
from proxies.cache_server.config import MAX_SIZE
from proxies.random_proxies.log import logger

def pop(conditions):
    search_query = {
        'size': MAX_SIZE,
        'query': conditions
    }
    try:
        # Get proxies which satisfy given conditions
        data = es.search(index='proxies', doc_type='proxy', body=search_query)
        proxies = data['hits']['hits']

        # Randomly select it
        proxy = choice(proxies)
        ip = proxy['_id']
        print('Selected proxy:', proxy)
        # Remove it from proxies index
        es.delete(index='proxies', doc_type='proxy', id=ip)

        # Add it to recents index
        es.index(index='recents', doc_type='proxy', id=ip, body=proxy['_source'])
    except Exception as e:
        template = 'An exception of type {0} occurred.\nArguments: {1!r}'
        message = template.format(type(e).__name__, e.args)
        logger.error(message)
        return None

    return ip
