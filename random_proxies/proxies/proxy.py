# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from random import choice

from random_proxies.proxies import settings
from random_proxies.proxies.utils import fetch, parse_response, country_to_code
from random_proxies.proxies.exception import NoSuchProxyError
from random_proxies.proxies.db import pop

def _select(proxies):
    if len(proxies) == 0:
        raise NoSuchProxyError('No proxy satisfying given conditions.')
    proxy = choice(proxies)
    
    return proxy['ip address'] + ':' + proxy['port']

def random_proxy(
    use_cache=True,
    protocol='http',
    standard=None,
    country=None,
    code=None
):
    conditions = {
        'country': country,
        'https': ('yes', 'no')[protocol == 'http'],
        'code': code,
        'anonymity': standard
    }

    if protocol == 'http':
        url = settings.BASE_URL
    elif protocol == 'https':
        url = settings.SSL_URL
    elif protocol == 'socks':
        url = settings.SOCKS_URL
        
    if not use_cache:
        res = fetch(url)
        proxies = parse_response(res, conditions)
        return _select(proxies)
    else:
        if protocol == 'socks':
            conditions['version'] = 'socks4'

        # Removing None conditions
        new_conditions = { k:v for k, v in conditions.items() if v != None}
            
        # County-code matching
        if code != None and country != None:
            if country_to_code(country, code):
                return pop(new_conditions)

        # Fetch from db
        return pop(new_conditions)
