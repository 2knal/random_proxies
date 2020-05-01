# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from random import choice

from random_proxies.cache import db
from random_proxies.proxies.log import logger
from random_proxies.proxies.exception import NoSuchProxyError

def pop(conditions):
    # Get proxies which satisfy given conditions
    proxies_collection = db['proxies']
    recents_collection = db['recents']

    proxies = proxies_collection.find(conditions)
    if proxies.count() == 0:
        raise NoSuchProxyError('No proxy satisfying given conditions.')
    
    # Randomly select it
    proxies = list(proxies)
    proxy = choice(proxies)
    ip = proxy['_id']
    
    try:
        # Remove it from proxies index
        proxies_collection.delete_one({ '_id': ip })

        # Add it to recents index
        recents_collection.insert_one(proxy)
    except Exception as e:
        template = 'An exception of type {0} occurred.\nArguments: {1!r}'
        message = template.format(type(e).__name__, e.args)
        logger.error(message)

    return ip
