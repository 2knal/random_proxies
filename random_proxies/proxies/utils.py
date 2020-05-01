# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup as bs

from functools import wraps
import errno
import os
import signal
import json 
from os.path import dirname, join
from random_proxies.proxies.log import logger
from random_proxies.proxies.exception import TimeoutError, CountryCodeError
from random_proxies.proxies import settings

def country_to_code(country, code):
    mapper = {}
    path = join(dirname(__file__), 'c2c.json')
    with open(path, 'r') as f:
        mapper = json.load(f)
    if mapper[country] == code:
        return True
    raise CountryCodeError('Country code does not match with the added country.')

# https://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish
def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator

# https://www.peterbe.com/plog/best-practice-with-retries-with-requests
def fetch(url=settings.BASE_URL,
    suffix='',
    backoff_factor=settings.HTTP_DELAY,
    status_forcelist=(500, 502, 504)):
    try:
        res = None
        with Session() as sess:
            retry = Retry(
                total=settings.HTTP_RETRIES,
                read=settings.HTTP_RETRIES,
                connect=settings.HTTP_RETRIES,
                backoff_factor=backoff_factor,
                status_forcelist=status_forcelist,
            )
            adapter = HTTPAdapter(max_retries=settings.HTTP_RETRIES)
            sess.mount('http://', adapter)
            sess.mount('https://', adapter)

            res = sess.get(url, timeout=settings.HTTP_TIMEOUT)
        return res.text
    except Exception as e:
        template = 'An exception of type {0} occurred.\nArguments: {1!r}'
        message = template.format(type(e).__name__, e.args)
        logger.error(message)
        return None

def parse_header(header):
    # Fetching field names
    fields = []
    for field in header.find_all('th'):
        name = field.get_text().strip()
        fields.append(name)
    return fields

# Do some condition checking here
def parse_values(body, fields, conditions):
    rows = body.find_all('tr')
    proxies = []
    for row in rows:
        proxy = {}
        values = row.find_all('td')
        flag = False
        for field, value in zip(fields, values):
            field = field.lower()
            value = value.get_text().strip().lower()

            # When using this routine for DB dump update
            if conditions == {}:
                proxy[field] = value
                continue

            if field == 'last checked':
                temp = field.split()
                if temp[1].startswith('second'):
                    proxy[field] = value
                    
                # Taking only proxies scanned before less than 20 minutes
                elif temp[1].startswith('minute') and int(temp[0]) < settings.LAST_CHECKED_THRESHOLD:
                    proxy[field] = value

            elif field == 'country':
                # Check if code is added or not
                if conditions.get('country')== None:
                    proxy[field] = value
                else:
                    if value.startswith(conditions.get('country')):
                        proxy[field] = value

            elif field == 'https' and conditions.get('https') == value:
                proxy[field] = value

            elif field == 'code':
                # First code must match country if both are not none
                if conditions.get('code') == None:
                    proxy[field] = value
                else:
                    if conditions.get('country') and country_to_code(conditions.get('country'), conditions.get('code')):
                        proxy[field] = value
                    elif conditions.get('code'):
                        proxy[field] = value

            elif field == 'anonymity':
                if conditions.get('anonymity') == None:
                    proxy[field] = value
                elif conditions.get('anonymity') == value:
                    proxy[field] = value

            elif field in ['ip address', 'port', 'google', 'version']:
                proxy[field] = value

            else:
                flag = True
                break
            
        if not flag:
            proxies.append(proxy)
    return proxies

# TODO
# Add to db after giving the response
# Use multiprocessing to do so
def parse_response(res, conditions):
    soup = bs(res, 'lxml')
    table = soup.find(id='proxylisttable')
    header = table.find('thead')

    fields = parse_header(header)
    body = table.find('tbody')

    proxies = parse_values(body, fields, conditions)

    return proxies
