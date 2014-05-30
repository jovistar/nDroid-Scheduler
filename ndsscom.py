import socket
import json
import os

class NdssCom():
    def __init__(self, host, port):
        self.address = (host, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def update_state(self, uid, state):
        if state not in ['b', 'm']:
            return 1

        data = {}
        data['request'] = 'update_state'
        data['uid'] = uid
        data['state'] = state

        result = self.do_com(data)
        if result['response'] != 0:
            return 1
        return 0

    def scan_uid(self, uid):
        return self.scan('uid', uid)

    def scan_file(self, path):
        return self.scan('file', path)

    def scan(self, scanType, scanData):
        if scanType not in ['file', 'uid']:
            return 1, ''

        if scanType == 'file':
            if not os.path.isfile(scanData):
                return 1, ''

        data = {}
        data['request'] = 'scan'
        data['scanType'] = scanType
        if scanType == 'uid':
            data['uid'] = scanData
        elif scanType == 'file':
            data['path'] = os.path.abspath(scanData)

        result = self.do_com(data)
        if result['response'] != 0:
            return result['response'], ''
        return 0, result['state']

    def report_uid(self, uid):
        return self.report('uid', uid)

    def report_file(self, path):
        return self.report('file', path)

    def report(self, reportType, reportData):
        return 1

    def create_item(self, path, state):
        data = {}
        if state not in ['b', 'm']:
            return 1

        if not os.path.isfile(path):
            return 1
        
        data['request'] = 'create_item'
        data['path'] = os.path.abspath(path)
        data['state'] = state

        result = self.do_com(data)
        if result['response'] != 0:
            return 1
        return 0

    def do_com(self, data):
        msg = json.dumps(data)
        self.s.sendto(msg, self.address)
        result, addr = self.s.recvfrom(40960)

        return json.loads(result)
