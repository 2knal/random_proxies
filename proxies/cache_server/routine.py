# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from elasticsearch import helpers

from time import time

from proxies.cache_server.config import es
from proxies.cache_server.config import fetch, parse_response
from proxies.cache_server.config import is_good_proxy
from proxies.cache_server.config import logger
from proxies.cache_server.config import BASE_URL, SSL_URL, SOCKS_URL    

def _add(proxies):
    actions = [
        {   
            "_index": "proxies",
            "_type" : "proxy", 
            "_id" : proxy['ip address'] + ':' + proxy['port'], 
            "doc": proxy
        }
        for proxy in proxies
    ]
    if proxies:
        try:
            tic = time()
            helpers.bulk(es, actions)
            tac = time()
            print('Time taken to add to index:', tac - tic)
        except Exception as e:
            template = 'An exception of type {0} occurred.\nArguments: {1!r}'
            message = template.format(type(e).__name__, e.args)
            logger.error(message)

def _check():
    urls = [BASE_URL, SSL_URL, SOCKS_URL]
    proxies = []
    # Fetch all the proxies from these urls
    for url in urls:
        res = fetch(url)
        # Passing empty conditions so that
        proxies.extend(parse_response(res, {}))

    # Check if they work
    working_proxies = []
    for proxy in proxies:
        ip = proxy['ip address'] + ':' + proxy['port']
        # Implies SOCKS proxy
        if 'version' in proxy:
            ip = version + '://' + ip
        protocol = ('http', 'https')[proxy['https'] == 'yes']

        try:
            # Only if it works
            if is_good_proxy(ip, protocol=protocol):
                working_proxies.append(proxy)
        except Exception as e:
            template = 'An exception of type {0} occurred.\nArguments: {1!r}'
            message = template.format(type(e).__name__, e.args)
            logger.error(message)
    
    return working_proxies

if __name__ == '__main__':
    tic = time()
    proxies = _check()
    # _add(proxies)
    tac = time()
    print('Total time:', tac - tic)