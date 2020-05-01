# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Will run after every 2 hours to add new proxies to 'proxies' collection

from time import time

from random_proxies.cache import db
from random_proxies.cache import fetch, parse_response
from random_proxies.cache import is_good_proxy
from random_proxies.cache import logger
from random_proxies.cache import BASE_URL, SSL_URL, SOCKS_URL    

def _check():
    urls = [BASE_URL, SSL_URL, SOCKS_URL]
    proxies = []

    # Fetch all the proxies from these urls
    for url in urls:
        res = fetch(url)
        # Passing empty conditions so that all proxies will be fetched
        proxies.extend(parse_response(res, {}))

    count = 0

    # proxies collection
    proxies_collection = db['proxies']

    # Check if they work
    for proxy in proxies:
        ip = proxy['ip address'] + ':' + proxy['port']

        # Adding _id to proxy document
        proxy['_id'] = ip
        protocol = ('http', 'https')[proxy['https'] == 'yes']

        # Implies SOCKS proxy
        if 'version' in proxy:
            ip = proxy['version'] + '://' + ip
            protocol = 'http'

        try:
            # Only if it works
            if is_good_proxy(ip, protocol=protocol):

                # Add it to proxies collection
                proxies_collection.insert_one(proxy)
                
        except Exception as e:
            template = 'An exception of type {0} occurred.\nArguments: {1!r}'
            message = template.format(type(e).__name__, e.args)
            logger.error(message)

if __name__ == '__main__':
    tic = time()
    _check()
    tac = time()
    print('Total time: [routine]', tac - tic)
