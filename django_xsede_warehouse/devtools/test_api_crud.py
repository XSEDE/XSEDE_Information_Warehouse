#!/usr/bin/env python
from __future__ import print_function
import argparse
import base64
import copy
import datetime
from datetime import datetime
import json
import os
import pprint
import pwd
import re
import shutil
import signal
import socket
import ssl
from ssl import _create_unverified_context
import sys
from time import sleep
from urlparse import urlparse

try:
    import http.client as httplib
except ImportError:
    import httplib

import pdb

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Test():
    def __init__(self):
        self.args = None

        parser = argparse.ArgumentParser(epilog='Example: <program> -u http://localhost:8000/glue2-db-api/v1/admindomain/ -k urn:glue2:AdminDomain:unsupported.xsede.org --a <username>:<password>')
        parser.add_argument('-k', '--key', action='store', dest='key', required=True, \
                            help='Existing document key')
        parser.add_argument('-u', '--url', action='store', dest='url', required=True, \
                            help='Base URL for test')
        parser.add_argument('-a', '--auth', action='store', dest='auth', required=True, \
                            help='Authentication username:password')
        parser.add_argument('-l', '--log', action='store', \
                            help='Logging level (default=warning)')
        parser.add_argument('--verbose', action='store_true', \
                            help='Verbose output')
        parser.add_argument('--pdb', action='store_true', \
                            help='Run with Python debugger')
        self.args = parser.parse_args()

        if self.args.pdb:
            pdb.set_trace()

        if self.args.url is None:
            eprint("Missing -u URL parameter")
            sys.exit(1)
        if self.args.key is None:
            eprint("Missing -k KEY parameter")
            sys.exit(1)
        if self.args.auth is None:
            eprint("Missing -a username:password parameter")
            sys.exit(1)

    def exit_signal(self, signal, frame):
        eprint('Caught signal, exiting...')
        sys.exit(0)

    def run(self):
        signal.signal(signal.SIGINT, self.exit_signal)

        print('Starting program=%s pid=%s, uid=%s(%s)' % \
                     (os.path.basename(__file__), os.getpid(), os.geteuid(), pwd.getpwuid(os.geteuid()).pw_name))
        URL = self.args.url
        print('URL: ' + URL)
        KEY = self.args.key
        print('KEY: ' + KEY)
        URLP = urlparse(URL)
        
        headers = {'Content-type': 'application/json',
                'Authorization': 'Basic %s' % base64.standard_b64encode(self.args.auth) }

        conn = httplib.HTTPConnection(URLP.hostname, URLP.port)
        
        GET_URL = '/'.join([URLP.path.rstrip('/'), 'ID', KEY]) + '/'
        print('** GET ' + GET_URL)
        conn.request('GET', GET_URL, None, headers)
        response = conn.getresponse()
        result = response.read()
        print('   status={} {}; bytes={}'.format(response.status, response.reason, len(result)))
        result_hash = json.loads(result)
        ORIG_DATA = copy.copy(result_hash['results'][0])
        ORIG_ID = ORIG_DATA['ID']
        if response.status != 404 and self.args.verbose:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(ORIG_DATA)
        else:
            print('   description=' + ORIG_DATA['Description'])
        
        ##########
        NEW_KEY = ORIG_ID + '.TEST1'
        NEW_DATA = copy.copy(ORIG_DATA)
        NEW_DATA['ID'] = NEW_KEY
        NEW_DATA['Description'] = 'POST Testing: ' + NEW_KEY
        POST_URL = '/'.join([URLP.path.rstrip('/')]) + '/'
        print('** POST ' + POST_URL + ' (ID=' + NEW_KEY + ')')
        NEW_STRING = json.dumps(NEW_DATA)
        conn.request('POST', POST_URL, NEW_STRING, headers)
        response = conn.getresponse()
        result = response.read()
        print('   status={} {}; bytes={}'.format(response.status, response.reason, len(result)))
        result_hash = json.loads(result)
        if response.status == 201:
            result_data = result_hash['results']
            if self.args.verbose:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(result_hash)
            else:
                print('   description=' + result_data['Description'])

        GET_URL = '/'.join([URLP.path.rstrip('/'), 'ID', NEW_KEY]) + '/'
        print('** GET ' + GET_URL)
        conn.request('GET', GET_URL, None, headers)
        response = conn.getresponse()
        result = response.read()
        print('   status={} {}; bytes={}'.format(response.status, response.reason, len(result)))
        result_hash = json.loads(result)
        if response.status == 200:
            result_data = result_hash['results'][0]
            if self.args.verbose:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(result_data)
            else:
                print('   description=' + result_data['Description'])

        NEW_DATA['Description'] = 'PUT Testing: ' + NEW_KEY
        PUT_URL = '/'.join([URLP.path.rstrip('/'), 'ID', NEW_KEY]) + '/'
        print('** PUT ' + PUT_URL)
        NEW_STRING = json.dumps(NEW_DATA)
        conn.request('PUT', PUT_URL, NEW_STRING, headers)
        response = conn.getresponse()
        result = response.read()
        print('   status={} {}; bytes={}'.format(response.status, response.reason, len(result)))
        result_hash = json.loads(result)
        if response.status == 201:
            result_data = result_hash['results']
            if self.args.verbose:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(result_hash)
            else:
                print('   description=' + result_data['Description'])

        GET_URL = '/'.join([URLP.path.rstrip('/'), 'ID', NEW_KEY]) + '/'
        print('** GET ' + GET_URL)
        conn.request('GET', GET_URL, None, headers)
        response = conn.getresponse()
        result = response.read()
        print('   status={} {}; bytes={}'.format(response.status, response.reason, len(result)))
        result_hash = json.loads(result)
        if response.status == 200:
            result_data = result_hash['results'][0]
            if self.args.verbose:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(result_data)
            else:
                print('   description=' + result_data['Description'])

        DELETE_URL = '/'.join([URLP.path.rstrip('/'), 'ID', NEW_KEY]) + '/'
        print('** DELETE ' + DELETE_URL)
        conn.request('DELETE', DELETE_URL, None, headers)
        response = conn.getresponse()
        result = response.read()
        print('   status={} {}; bytes={}'.format(response.status, response.reason, len(result)))
        if self.args.verbose:
            print(result)

        print('** GET ' + GET_URL)
        conn.request('GET', GET_URL, None, headers)
        response = conn.getresponse()
        result = response.read()
        print('   status={} {}; bytes={}'.format(response.status, response.reason, len(result)))
        result_hash = json.loads(result)
        if response.status == 200:
            result_data = result_hash['results'][0]
            if self.args.verbose:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(result_data)
            else:
                print('   description=' + result_data['Description'])

if __name__ == '__main__':
    my_test = Test()
    status = my_test.run()
    sys.exit(0)
