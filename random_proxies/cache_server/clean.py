# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from elasticsearch import helpers

from time import time

from random_proxies.cache_server.config import es
from random_proxies.cache_server.config import is_good_proxy
from random_proxies.cache_server.config import logger
from random_proxies.cache_server.utils import add

def _clean():
    # Get all the proxies from proxies index
    data = es.search(index='proxies', doc_type='proxy', body={'size': })
    proxies = data['hits']['hits']
    
    # Delete those which arent good
    for proxy in proxies:
        ip = proxy['ip address'] + ':' + proxy['port']
        protocol = ('http', 'https')[proxy['https'] == 'yes']
        
        # Implies SOCKS proxy
        if 'version' in proxy:
            ip = proxy['version'] + '://' + ip
            protocol = 'http'
        try:
            # If it doesn't work
            if not is_good_proxy(ip, protocol=protocol):
                # Delete from proxies index
                es.delete(index='proxies', doc_type='proxy', id=ip)
            
        except Exception as e:
            # Delete from proxies index
            es.delete(index='proxies', doc_type='proxy', id=ip)
            template = 'An exception of type {0} occurred.\nArguments: {1!r}'
            message = template.format(type(e).__name__, e.args)
            logger.error(message)

if __name__ == '__main__':
    tic = time()
    _clean()
    tac = time()
    print('Total time: [clean]', tac - tic)