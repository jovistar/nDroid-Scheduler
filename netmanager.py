from twisted.internet.protocol import DatagramProtocol
from ndlcom import NdlCom
from ndacom import NdaCom
from ndscom import NdsCom
from msgmanager import MsgManager
import ndutil
import os
import shutil

class NetManager(DatagramProtocol):
    def set_msgmanager(self, msgManager):
        self.msgManager = msgManager

    def set_ndlcom(self, ndlCom):
        self.ndlCom = ndlCom

    def set_ndscom(self, ndsCom):
        self.ndsCom = ndsCom

    def set_ndacom(self, ndaCom):
        self.ndaCom = ndaCom

    def datagramReceived(self, data, (host, port)):
        retCode, result = self.msgManager.res_request(data)
        if retCode != 0:
            self.ndlCom.do_com('Bad Request From %s:%d' % (host, port))
        else:
            responseData = None
            self.ndlCom.do_com('Request: %s From %s:%d' % (result['request'], host, port))
            if result['request'] == 'scan':
                responseData = self.dispatch_scan(result)
            elif result['request'] == 'report':
                responseData = self.dispatch_report(result)
            elif result['request'] == 'create_item':
                responseData = self.dispatch_create_item(result)
            elif result['request'] == 'update_state':
                responseData = self.dispatch_update_state(result)

            msg = self.msgManager.gen_response(responseData)
            self.transport.write(msg, (host, port))

    def dispatch_scan(self, data):
        if data.get('scanType') == None:
            return self.gen_response_error(1)

        scanType = data.get('scanType')
        uid = None
        path = None
        if scanType == 'uid':
            if data.get('uid') == None:
               return self.gen_response_error(1)
            uid = data.get('uid')
        elif scanType == 'file':
            if data.get('path') == None:
               return self.gen_response_error(1)
            path = data.get('path')
        else:
            return self.gen_response_error(1)

        responseData = {}
        if scanType == 'uid':
            retCode, result = self.ndaCom.get_item_state(uid)
            if retCode != 0:
                return self.gen_response_error(2)
            responseData['response'] = 0
            responseData['state'] = result
        elif scanType == 'file':
            if os.path.isabs(path) == False:
                return self.gen_response_error(1)
            if os.path.isfile(path) == False:
                return self.gen_response_error(1)
            
            retCode, result = self.ndsCom.create_item(path)
            if retCode != 0:
                return self.gen_response_error(1)
            uid = result

            retCode, result = self.ndaCom.get_item_state(uid)
            if retCode == 0:
                responseData['response'] = 0
                responseData['state'] = result
                return responseData

            retCode = self.ndaCom.create_item(uid, 'u')
            responseData['response'] = 0
            responseData['state'] = 'u'

            #here
        return responseData

    def dispatch_report(self, data):
        responseData = {}

        return self.gen_response_error(1)

    def dispatch_create_item(self, data):
        responseData = {}

        if data.get('path') == None or data.get('state') == None:
            return self.gen_response_error(1)

        path = data.get('path')
        state = data.get('state')

        if os.path.isabs(path) == False:
            return self.gen_response_error(1)

        if os.path.isfile(path) == False:
            return self.gen_response_error(1)

        if state not in ['b', 'm']:
            return self.gen_response_error(1)

        retCode, result = self.ndsCom.create_item(path)
        if retCode != 0:
            return self.gen_response_error(1)
        uid = result

        retCode = self.ndaCom.create_item(uid, state)
        if retCode != 0:
            return self.gen_response_error(1)
        responseData['response'] = 0
        return responseData

    def dispatch_update_state(self, data):
        if data.get('uid') == None or data.get('state') == None:
            return self.gen_response_error(1)

        uid = result['uid']
        state = result['state']

        if state not in ['b', 'm']:
            return self.gen_response_error(1)

        retCode = self.ndaCom.do_com(uid, state)
        if retCode != 0:
            return self.gen_response_error(1)
        return 0

    def gen_response_error(self, retCode):
        responseData = {}
        responseData['response'] = retCode
        return responseData
