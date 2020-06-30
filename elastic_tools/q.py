#!/usr/bin/env python3

import http.client as httplib
import json
import ssl
import sys

import pdb

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class ES():
    def __init__(self):
        host = 'localhost'
        port = '9200'
        self.CONN = httplib.HTTPConnection(host=host, port=port)
        self.URL = '/resourcev3-index/_search?pretty=true'
        self.HEADERS = {'Content-Type': 'application/json'
        }
        
        self.Q1 = {
            'from': 0,
            'size': 9999,
            'query': {
                'bool': {
                    'filter': [
                        {'term': { 'QualityLevel': 'Production' }},
                        {'nested': {
                            'path': 'Relations',
                            'query': {
                                'bool': {
                                    'filter': [
                                        {'term': {
                                            'Relations.RelatedID.keyword': 'urn:ogf:glue2:info.xsede.org:resource:rsp:support.organizations:drupalnodeid:1553'
                                        } }
                                    ]
                                }
                            }
                        } }
                    ]
                }
            }
        }

        self.Q2 = {
            'from': 0,
            'size': 9999,
            'query': {
                'bool': {
                    'filter': [
                        {'term': { 'QualityLevel': 'Production' }},
                        {'bool': {
                            'must_not':
                                {'nested': {
                                    'path': 'Relations',
                                    'query': {
                                        'bool': {
                                            'filter': [
                                                {'term': {
                                                    'Relations.RelatedID.keyword': 'urn:ogf:glue2:info.xsede.org:resource:rsp:support.organizations:drupalnodeid:1553'
                                                } }
                                            ]
                                        }
                                    },
                                } }
                        } }
                    ]
                }
            }
        }

        self.Q3 = {
            'from': 0,
            'size': 9999,
            'query': {
                'bool': {
                  'filter': [
                    {
                      'bool': {
                        'filter': [
                          {
                            'bool': {
                                'must': {
                                    'term': { 'QualityLevel': 'Production' }
                                }
                            }
                          },
                          {
                            'nested': {
                              'path': 'Relations',
                              'score_mode': 'max',
                              'query': {
                                'bool': {
                                  'should': [
                                    {
                                      'match_phrase': {
                                        'Relations.RelatedID': 'urn:ogf:glue2:info.xsede.org:resource:rsp:support.organizations:drupalnodeid:1553'
                                      }
                                    }
                                  ],
                                  'minimum_should_match': 1
                                }
                              },
                              'score_mode': 'none'
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
            }
        }

    def run(self, query):
        query_string = json.dumps(query)
        self.CONN.request('GET', self.URL, query_string, self.HEADERS)
        response = self.CONN.getresponse()
        data_raw = response.read().decode('utf-8-sig')
        try:
            data_json = json.loads(data_raw)
        except ValueError as e:
            eprint('Response not in expected JSON format ({})'.format(e))
            sys.exit(1)
        try:
            return(len(data_json['hits']['hits']))
        except:
            print(data_raw)
        
if __name__ == '__main__':
    pdb.set_trace()
    e = ES()
    results = e.run(e.Q1)
    print('Q1 hits = {}'.format(results))
    results = e.run(e.Q2)
    print('Q2 hits = {}'.format(results))
    results = e.run(e.Q3)
    print('Q3 hits = {}'.format(results))

#FOO='
#{
#  "from": 0,
#  "query": {
#    "bool": {
#      "must": [{"term": {"QualityLevel": "Production" }},
#                  {"nested": {"path": "Relations",
#                               "query": {"terms": {"Relations.RelatedID": ["urn:ogf:glue2:info.xsede.org:resource:rsp:support.organizations:drupalnodeid:1553"]}}
#                  }}
#      ]
#    }},
#  "size": 9999
#}'
