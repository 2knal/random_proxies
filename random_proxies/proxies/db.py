# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from random import choice

from random_proxies.cache_server.config import es
from random_proxies.cache_server.config import MAX_SIZE
from random_proxies.proxies.log import logger
from random_proxies.proxies.exception import NoSuchProxyError

def pop(conditions):
    search_query = {
        'size': MAX_SIZE,
        'query': conditions
    }

    # Get proxies which satisfy given conditions
    data = es.search(index='proxies', doc_type='proxy', body=search_query)
    proxies = data['hits']['hits']

    if len(proxies) == 0:
        raise NoSuchProxyError('No proxy satisfying given conditions.')
    
    # Randomly select it
    proxy = choice(proxies)
    ip = proxy['_id']
    
    # Remove it from proxies index
    es.delete(index='proxies', doc_type='proxy', id=ip)

    # Add it to recents index
    es.index(index='recents', doc_type='proxy', id=ip, body=proxy['_source'])

    return ip
