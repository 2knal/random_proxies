# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import requests

import random_proxies.proxies.settings as settings
from random_proxies.proxies.utils import timeout
from random_proxies.proxies.log import logger

@timeout(seconds=settings.HTTP_TIMEOUT)
def is_good_proxy(ip, protocol='http'):   
    proxies = {
        'http': 'http://' + ip,
    }
    
    if protocol == 'https':
        proxies['https'] = 'https://' + ip

    url = settings.TEST_URL
    try:
        res = requests.get(url, proxies=proxies)
        if res.status_code == 200:
            return True
        return False
    except Exception as e:
        template = 'An exception of type {0} occurred.\nArguments: {1!r}'
        message = template.format(type(e).__name__, e.args)
        logger.error(message)
        return False

