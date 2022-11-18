#This sets up our references

import logging
from logging.config import dictConfig
import hashlib
import sys
import time

from flask import Flask, request,jsonify

from cdrinfo_lib import CDRInfo

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

def create_app(test_config=None):
    app = Flask(__name__)

    with app.app_context():
        global expert
        logging.info('Initializing.')
        expert = CDRInfo()
        logging.info('Expert system initialized.')

    @app.route("/cdrinfo/<searchTerm>", methods=['POST'])
    def cdrInfo(searchTerm):
        ipaddress = request.remote_addr
        requeststring = str(dict(request.form))
        requesthash = str(hashlib.md5(requeststring.encode('utf-8')).hexdigest())
        if request.method == 'POST':
            #time.sleep(2)
            logging.info('POST DrugInfo Request: {0} from IP: {1} MD5Sum: {2}'.format(searchTerm,ipaddress,requesthash))
            try:
                response = {}


                response = jsonify(response)
                logging.info('POST DrugInfo Response for Request {0}: {1}'.format(requesthash,str(response)))

            except KeyError:
                response = jsonify({'status': 'Invalid search Term'})
                logging.debug('Invalid search Term {0}'.format(requesthash))
        else:
            response = jsonify({'status': 'Route exists'})
            logging.info('Non-POST request')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method, Access-Control-Allow-Origin, Access-Control-Allow-Methods')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Vary','Origin')
        #response.headers.add('Access-Control-Allow-Headers', '*')
        #response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route("/status/")
    def status():
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        response.headers.add('Access-Control-Allow-Headers', 'X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method, Access-Control-Allow-Origin, Access-Control-Allow-Methods')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Vary','Origin')
        #response.headers.add('Access-Control-Allow-Headers', '*')
        #response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    return app


