'''
(Once the package is published)
pip install random-proxies 
    or 
Follow example usage to import the package
'''

from random_proxies import random_proxy

'''
Fetch directly from free-proxy-list.net

:param use_cache: Boolean value to fetch from cache_server or not (default: True)
:return: returns `ip:port`
:rtype: str
'''
random_proxy(use_cache=False)

'''
Fetch by protocol name.

:param protocol: Protocol name, either http, https or socks (default: http)
:return: returns `ip:port`
:rtype: str
'''
random_proxy(protocol='https')

'''
Fetch by country name or code.

:param country: Country name (default: None)
:param code: Country code, should match with country name if added (default: None)
:return: returns `ip:port`
:rtype: str
'''
random_proxy(country='india')
random_proxy(code='in')

'''
Fetch by proxy standard.

:param standard: Proxy standard, either anonymous, elite proxy, transparent (default: anonymous)
:return: returns `ip:port`
:rtype: str
'''
random_proxy(standard='elite proxy')
