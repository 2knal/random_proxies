# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from random import choice

import proxies.random_proxies.settings as settings
from proxies.random_proxies.utils import fetch, parse_response
from proxies.random_proxies.exception import NoSuchProxyError

def _select(proxies):
    if len(proxies) == 0:
        raise NoSuchProxyError('No proxy satisfying given conditions.')
    proxy = choice(proxies)
    print('Selected proxy:', proxy, '\nLength:', len(proxies))
    return proxy['ip address'] + ':' + proxy['port']

def random_proxy(
    use_cache=True,
    protocol='http',
    standard='anonymous',
    country=None,
    code=None
):
    if not use_cache:
        conditions = {
            'country': country,
            'https': ('yes', 'no')[protocol == 'http'],
            'code': code
        }

        if protocol == 'http':
            url = settings.BASE_URL
            conditions['anonymity'] = standard
        elif protocol == 'https':
            url = settings.SSL_URL
            conditions['anonymity'] = standard
        elif protocol == 'socks':
            url = settings.SOCKS_URL
        
        res = fetch(url)
        print('Conditions:', conditions)
        proxies = parse_response(res, conditions)
        return _select(proxies)
    else:
        # Fetch from db
        pass
    
