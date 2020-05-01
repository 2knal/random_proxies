# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Will run after every 4 hours to update 'recents' collection

from time import time

from random_proxies.cache import db
from random_proxies.cache import is_good_proxy
from random_proxies.cache import logger

def _check():
    recents_collection = db['recents']
    proxies_collection = db['proxies']

    # Check if proxies are working in recents index
    recents = collection.find({})
    for proxy in recents:

        ip = proxy['_id']
        protocol = ('http', 'https')[proxy['https'] == 'yes']
        
        # Implies SOCKS proxy
        if 'version' in proxy:
            ip = proxy['version'] + '://' + ip
            protocol = 'http'

        try:
            # Only if it works
            if is_good_proxy(ip, protocol=protocol):
                # Delete from recents
                recents_collection.delete_one({'_id': ip})

                # Add them to proxies
                proxies_collection.insert_one(proxy)

        except Exception as e:
            # Delete from recents
            recents_collection.delete_one({'_id': ip})
            template = 'An exception of type {0} occurred.\nArguments: {1!r}'
            message = template.format(type(e).__name__, e.args)
            logger.error(message)
            

if __name__ == '__main__':
    tic = time()
    _check()
    tac = time()
    print('Total time: [update]', tac - tic)