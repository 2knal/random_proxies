# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from random_proxies.cache import db
from random_proxies.cache import logger

import os
from os.path import join, dirname
from random import choice
from flask import Flask, request, jsonify
from markdown import markdown

app = Flask(__name__)

@app.route('/')
def index():
    try:
        with open(join(dirname(__file__), 'README.md')) as f:
            markdown_file = f.read()
            return markdown(markdown_file)
    except Exception as e:
        return "It works"

@app.route('/fetch', methods=['GET'])
def fetch():
    conditions = request.args
    proxies_collection = db['proxies']
    recents_collection = db['recents']

    # Fetch from proxies
    proxies = proxies_collection.find(conditions)
    if proxies.count() == 0:
        return jsonify({ 'success': 'no' })
    
    # Randomly select it
    proxies = list(proxies)
    proxy = choice(proxies)
    ip = proxy['_id']
    
    try:
        # Remove it from proxies index
        proxies_collection.delete_one({ '_id': ip })

        # Add it to recents index
        recents_collection.insert_one(proxy)

        return jsonify({ 'ip': ip, 'success': 'yes' })

    except Exception as e:
        template = 'An exception of type {0} occurred.\nArguments: {1!r}'
        message = template.format(type(e).__name__, e.args)
        logger.error(message)
        return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)