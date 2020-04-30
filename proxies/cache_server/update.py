# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from elasticsearch import helpers

from time import time

from proxies.cache_server.config import es
from proxies.cache_server.config import fetch, parse_response
from proxies.cache_server.config import is_good_proxy
from proxies.cache_server.config import logger
from proxies.cache_server.utils import add
from proxies.cache_server.config import BASE_URL, SSL_URL, SOCKS_URL, MAX_SIZE   

def _check():
    # Check if proxies are working in recents index
    data = es.search(index='recents', doc_type='proxy', body={'size': })
    recents = data['hits']['hits']
    add_back_proxies = []
    if recents:
        for proxy in recents:
            proxy = proxy['_source']['doc']
            try:
                # Only if it works
                if is_good_proxy(ip, protocol=protocol):
                    add_back_proxies.append(proxy)
            except Exception as e:
                template = 'An exception of type {0} occurred.\nArguments: {1!r}'
                message = template.format(type(e).__name__, e.args)
                logger.error(message)
            
    # If yes, then add them back to proxies index
    if add_back_proxies:
        add(add_back_proxies, 'recents')

if __name__ == '__main__':
    tic = time()
    _check()
    tac = time()
    print('Total time: [update]', tac - tic)