# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
from os.path import join, dirname
from dotenv import load_dotenv

from pymongo import MongoClient

env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

uri = os.environ.get('MONGO_URI')

conn = MongoClient(uri)
db = conn['random_proxies']

# Remove circular import
from random_proxies.proxies.log import logger
from random_proxies.proxies.proxy_health import is_good_proxy
from random_proxies.proxies.settings import BASE_URL, SOCKS_URL, SSL_URL
from random_proxies.proxies.utils import fetch, parse_response
