# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Will run every day at 12 am to check for working proxies

from time import time

from random_proxies.cache import db
from random_proxies.cache import is_good_proxy
from random_proxies.cache import logger

def _clean():
    # Get all the proxies from proxies collection
    collection = db['proxies']
    proxies = collection.find({})
    
    # Delete those which arent good
    for proxy in proxies:
        ip = proxy['_id']
        protocol = ('http', 'https')[proxy['https'] == 'yes']
        
        # Implies SOCKS proxy
        if 'version' in proxy:
            ip = proxy['version'] + '://' + ip
            protocol = 'http'
        try:
            # If it doesn't work
            if not is_good_proxy(ip, protocol=protocol):
                # Delete from proxies collection
                collection.delete_one({'_id': ip})
            
        except Exception as e:
            # Delete from proxies collection
            collection.delete_one({'_id': ip})
            template = 'An exception of type {0} occurred.\nArguments: {1!r}'
            message = template.format(type(e).__name__, e.args)
            logger.error(message)

if __name__ == '__main__':
    tic = time()
    _clean()
    tac = time()
    print('Total time: [clean]', tac - tic)
