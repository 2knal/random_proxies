# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import requests
from random_proxies.proxies.settings import CACHE_SERVER_URL

def pop(conditions):
    query_string = '?'

    for k, v in conditions.items():
        query_string += f'{k}={v}&'
    url = CACHE_SERVER_URL + query_string[:-1]
    data = requests.get(url).text
    data = json.loads(data)

    return data['ip']
