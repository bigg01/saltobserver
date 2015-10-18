#!/usr/bin/env python
#! -*- coding: utf-8 -*
from __future__ import print_function

__author__ = "Oliver Guggenbuehl"
__license__ = "GPL"
__version__ = "1.0.1"
__status__ = "Development"

# imports
try:
    import requests
except:
    print("cannot import requests")
import json
import pprint
import logging
import httplib

# debug
debug = False

if debug:
    # request logger
    httplib.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True




class SaltApiManager(object):
    '''
    SaltApiManager abstracts an saltapi request
    '''
    def __init__(self, user, password, SALT_API='http://localhost', PORT='8000'):
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        #'Content-Type': 'application/json'
        self._SALT_API = '{0}:{1}'.format(SALT_API, PORT)
        self.username = user
        self.password = password
        self.headers['X-Auth-Token'] = self.login()

    def __str__(self):
        return self._SALT_API

    def login(self):
        self.data = {
            'eauth': 'pam',
            'username': self.username,
            'password': self.password
        }
        #print(json.dumps(data))
        self.r = requests.post(self._SALT_API + '/login',
                               data=json.dumps(self.data),
                               headers=self.headers
                               )
        if self.r.status_code == 200:
            print('connect to saltapi!')
            #logging.INFO('connect to saltapi!')
            if debug:
                print(self.r.text)
            return self.r.json()['return'][0]['token']
        else:
            print('can not connect to saltapi!!!')

    def logout(self):
        """
        self.data = {
            'eauth': 'pam',
            'username': self.username,
            'password': self.password
        }
        """
        #print(json.dumps(data))
        self.r = requests.post(self._SALT_API + '/logout',
                               data=json.dumps(self.data),
                               headers=self.headers
                               )
        if self.r.status_code == 200:
            print('Logout from: ' + self._SALT_API)
            if debug:
                print(self.r.text)
            return self.r.text
        else:
            print('cannot logout!!!')


    def run(self, tgt, fun='test.ping', arg=None):
        """
        curl -si http://10.0.0.4:8000 \
        -H "Accept: application/x-yaml" \
        -H "X-Auth-Token: 09e15bfd2abd70312367d6d458a380ed2198c9c9" \
        -d client=local \
        -d tgt='*' \
        -d fun='test.ping' \

        """
        self.data = {
            'tgt': tgt,
            'fun': fun,
            'client': 'local',
        }
        if arg:
            self.data['arg'] = arg

        if debug:
            print(self.data)

            #print(json.dumps(data))
            print(self.headers)
        self.r = requests.post(self._SALT_API,
                          data=json.dumps(self.data),
                          headers=self.headers
                          )
        print(self.r.status_code)
        if self.r.status_code == 200:
            self.minion_return = self.r.json()['return'][0]
            if isinstance(self.minion_return, dict):
                for minion in self.minion_return:
                    print(minion)
                    print(self.minion_return.get(minion))
            elif isinstance(self.minion_return, str):
                for minion in self.minion_return:
                    print(minion)
                    print(self.minion_return.get(minion))

        else:
            print('return error')
            print(self.r.text)

    def listkeys(self):
        self.data = {
            'fun': 'key.list_all',
            'client':'wheel',
            'tgt':'*',
            'match': ''
        }
        #print(json.dumps(data))
        self.r = requests.post(self._SALT_API + '/',
                          data=json.dumps(self.data),
                          headers=self.headers
                          )
        #print(r.text)
        print(self.r.status_code)
        if self.r.status_code == 200:
            #print(r.text)
            for key in self.r.json()['return'][0]['data']['return']['minions']:
                print(key)
            #return r.json()['return'][0]

#run()

if __name__ == '__main__':
    saltrun = SaltApiManager(user = 'guo',
                          password = 'viper1',
                          SALT_API = 'http://10.0.0.4',
                          PORT = '8000'
                          )
    saltrun.listkeys()
    saltrun.run(tgt='*', fun= 'user.info', arg='guo')
    saltrun.run(tgt='*', fun= 'status.loadavg')
    saltrun.logout()
    #saltrun.run(tgt='*', fun= 'cmd.run', arg='ls')

"""
payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
>>> r = requests.get("http://httpbin.org/get", params=payload)
"""


"""
% curl -si https://localhost:8000 \
        -H "Accept: application/x-yaml" \
        -H "X-Auth-Token: d40d1e1e" \
        -d client=local \
        -d tgt='*' \
        -d fun='test.ping' \
        -d arg
"""