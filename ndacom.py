#!/usr/bin/python

import socket
import json
import os

class NdaCom():
    def __init__(self, host, port):
        self.address = (host, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def create_item(self, uid, state):
        data = {}
        if state not in ['b', 'm', 'u']:
            return 1

        data['request'] = 'create_item'
        data['uid'] = uid
        data['state'] = state

        result = self.do_com(data)
        if result['response'] != 0:
            return 1
        return 0

    def delete_item(self, uid):
        data = {}
        
        data['request'] = 'delete_item'
        data['uid'] = uid

        result = self.do_com(data)
        if result['response'] != 0:
            return 1
        return 0

    def do_com(self, data):
        msg = json.dumps(data)
        self.s.sendto(msg, self.address)
        result, addr = self.s.recvfrom(40960)
        
        return json.loads(result)

    def update_item_state(self, uid, state):
        data = {}
        if state not in ['b', 'm', 'u']:
            return 1

        data['request'] = 'update_state'
        data['uid'] = uid
        data['state'] = state

        result = self.do_com(data)
        if result['response'] != 0:
            return 1
        return 0

    def get_item(self, uid):
        data = {}

        data['request'] = 'get_item'
        data['uid'] = uid

        result = self.do_com(data)
        if result['response'] != 0:
            return 1, ()
        return 0, data['item']

    def get_item_state(self, uid):
        data = {}

        data['request'] = 'get_state'
        data['uid'] = uid
     
        result = self.do_com(data)
        if result['response'] != 0:
            return 1, ''
        return 0, result['state']

    def get_item_last_update(self, uid):
        data = {}

        data['request'] = 'get_last_update'
        data['uid'] = uid

        result = self.do_com(data)
        if result['response'] != 0:
            return 1, ''
        return 0, result['last_update']
