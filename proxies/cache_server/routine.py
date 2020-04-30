# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from elasticsearch import helpers

from time import time

from proxies.cache_server.config import es
from proxies.cache_server.config import fetch, parse_response
from proxies.cache_server.config import is_good_proxy
from proxies.cache_server.config import logger
from proxies.cache_server.utils import add
from proxies.cache_server.config import BASE_URL, SSL_URL, SOCKS_URL    

def _check():
    urls = [BASE_URL, SSL_URL, SOCKS_URL]
    proxies = []
    # Fetch all the proxies from these urls
    for url in urls:
        print('URL:', url)
        res = fetch(url)
        # Passing empty conditions so that
        proxies.extend(parse_response(res, {}))

    print('Total proxies: ', len(proxies))
    # Check if they work
    working_proxies = []
    count = 0
    for proxy in proxies:
        count += 1
        print('Proxy count:', count)
        ip = proxy['ip address'] + ':' + proxy['port']
        protocol = ('http', 'https')[proxy['https'] == 'yes']

        # Implies SOCKS proxy
        if 'version' in proxy:
            ip = proxy['version'] + '://' + ip
            protocol = 'http'

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
    add(proxies, 'proxies')
    tac = time()
    print('Total time: [routine]', tac - tic)