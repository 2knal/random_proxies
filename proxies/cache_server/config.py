# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
from os.path import join, dirname
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

env_path = join(dirname(__file__), '.env')
# print('ENV PATH:', env_path)
load_dotenv(env_path)

# GLOBALS
elastic_password = os.environ.get('ELASTIC_PASSWORD')
elastic_username = 'elastic'

elastic_uri = 'http://localhost:9200'
MAX_SIZE = 10000

# Setting up conn
es = Elasticsearch([elastic_uri], http_auth=(elastic_username, elastic_password))

# Creating necessary index
if not es.indices.exists(index='proxies'):
    es.indices.create(index='proxies', ignore=400)

if not es.indices.exists(index='recents'):
    es.indices.create(index='recents', ignore=400)

from proxies.random_proxies.settings import BASE_URL, SSL_URL, SOCKS_URL
from proxies.random_proxies.log import logger
from proxies.random_proxies.utils import fetch, parse_response
from proxies.random_proxies.proxy_health import is_good_proxy