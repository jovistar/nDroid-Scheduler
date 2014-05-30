#!/usr/bin/python

from cnfmanager import CnfManager
from msgmanager import MsgManager
from ndlcom import NdlCom
from ndscom import NdsCom
from ndacom import NdaCom
from netmanager import NetManager
import ndutil
import getopt
import sys

from twisted.internet import reactor

def ndss_loop(doInit):
    ndutil.set_timezone()

    ndlCom = NdlCom('nDroid-Scheduler', '127.0.0.1', 12322)
    ndlCom.do_com('Initiating')

    ndlCom.do_com('Loading Configuration')
    cnfManager = CnfManager()
    cnfManager.load('./ndss.cnf')
    cnfData = cnfManager.get_cnf_data()

    if doInit:
        pass

    msgManager = MsgManager()

    ndsCom = NdsCom('127.0.0.1', 12321)
    ndaCom = NdaCom('127.0.0.1', 12323)

    netManager = NetManager()
    netManager.set_msgmanager(msgManager)
    netManager.set_ndlcom(ndlCom)
    netManager.set_ndscom(ndsCom)
    netManager.set_ndacom(ndaCom)

    reactor.listenUDP(cnfData['comPort'], netManager)
    ndlCom.do_com('Listening Com Port %d' % cnfData['comPort'])
    reactor.run()

if __name__ == '__main__':
    ndss_loop(False)
