'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  




class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
    	csv_file = csv.DictReader(open(policyFile, 'rb'), delimiter=',', quotechar='"')
 	
	for line in csv_file:
		msg = of.ofp_flow_mod()
		msg.priority = 65535
		msg.match.dl_src = EthAddr(line['mac_0'])
		msg.match.dl_dst = EthAddr(line['mac_1'])
		event.connection.send(msg)
		log.debug("Dropping packets from %s to %s", line['mac_0'], line['mac_1'])
    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
