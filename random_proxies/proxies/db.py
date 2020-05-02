# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import requests

from random_proxies.proxies.settings import CACHE_SERVER_URL
from random_proxies.proxies.exception import NoSuchProxyError

def pop(conditions):
    query_string = '?'

    for k, v in conditions.items():
        query_string += f'{k}={v}&'
    url = CACHE_SERVER_URL + query_string[:-1]
    data = requests.get(url).text
    data = json.loads(data)

    if data['success'] == 'yes':
        return data['ip']
    else:
        raise NoSuchProxyError('No proxy satisfying given conditions.')
