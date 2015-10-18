#!/usr/bin/env python
#! -*- coding: utf-8 -*

import requests
import json
import pprint


class SaltManager(object):
    def __init__(self, user, password, SALT_API='http://localhost', PORT='8000'):
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self._SALT_API = '{0}:{1}'.format(SALT_API, PORT)
        self.username = username
        self.password = password
        self.headers['X-Auth-Token'] = self.login()

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
            print(r.text)
            return r.json()['return'][0]['token']
        else:
            print('can not connect to saltapi!!!')

    def listkeys(self):
        self.data = {
            'fun': 'key.list_all',
            'client':'wheel',
            'tgt':'*',
            'match': ''
        }
        #print(json.dumps(data))
        self.r = requests.post(self.SALT_API + '/',
                          data=json.dumps(self.data),
                          headers=self.headers
                          )
        #print(r.text)
        print(self.r.status_code)
        if self.r.status_code == 200:
            #print(r.text)
            for key in self.r.json()['return'][0]['data']['return']['minions']:
                print key
            #return r.json()['return'][0]
"""
def listkeys_delete():
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    headers['X-Auth-Token'] = login()
    data = {'fun': 'key.delete','client':'wheel','tgt':'*','match': ''}

    #print(json.dumps(data))
    r = requests.post(SALT_API + '/', data=json.dumps(data), headers=headers)
    print(r.text)
    if r.status_code == 202:
        print(r.text)


def run():
    headers = {'Accept': 'application/x-yaml', 'Content-Type': 'application/json'}
    headers['X-Auth-Token'] = login()
    data = {'tgt': '*', 'fun': 'status.diskusage'}

    #print(json.dumps(data))
    r = requests.post(SALT_API + '/minions', data=json.dumps(data), headers=headers)

    if r.status_code == 202:
        print(r.text)

        #print(r.json())
        #return r.json().get('return')[0]

def minions():
    """
    if 'salt-token' in session:
        print('Token is %s' % session['salt-token'])
    else:
        return redirect(url_for('login'))
    """
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    headers['X-Auth-Token'] = login()

    r = requests.get(SALT_API + '/minions', headers=headers)
    #r = requests.post(SALT_API + '/minions', headers=headers, data=payload)
    #r = requests.post(SALT_API + '/minions?tgt=*&fun=status.diskusage', headers=headers)

    print(r.url)
    print r.status_code

    r = requests.get(SALT_API + '/jobs', headers=headers)
    #r = requests.post(SALT_API + '/minions', headers=headers, data=payload)
    #r = requests.post(SALT_API + '/minions?tgt=*&fun=status.diskusage', headers=headers)

    print(r.url)
    print r.status_code
    print r.json()
    #minionmap = r.json()['return'][0]
    #print(r.json()['return'][0])
    #print(json.dumps(minionmap))
    # transform { minionid: {prop1: 'val1', ..}, ...} into
    # [{id: 'minionid', prop1: 'val1', ...}, ...]
    #minions = [dict(v, id=k) for k,v in minionmap.items()]
    #pprint.pprint(minions)
    #return json.dumps(minions)
"""
"""
% curl -sS localhost:8000/login \
    -H 'Accept: application/x-yaml'
    -d username='saltdev'
    -d password='saltdev'
    -d eauth='pam'
"""

#run()
saltrun = SaltManager(user = 'guo',
                      password = 'viper1',
                      SALT_API = 'http://10.0.0.4',
                      PORT = '8000'
                      )
saltrun.listkeys()

"""
payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
>>> r = requests.get("http://httpbin.org/get", params=payload)
"""