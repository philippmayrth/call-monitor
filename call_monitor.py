#!/usr/bin/env python

"""
	Notifications require OS X v10.9
	
    State controll keys for your fritz.box voipAPI:
        Activate: #96*5*
        Dissable: #96*4*
"""

import os
import re
import logging
from telnetlib import Telnet


class notifier:
    def notify(self, title="call monitor", message="a event occured"):
        assambled = 'osascript -e \'display notification \"{0}\" with title \"{1}\"\''.format(message, title)
        logging.info('Assambled comand for notification: {0}'.format(assambled))
        os.system(assambled)


class voip:
    only_number = re.compile('.*RING;\d*;(\d*);.*')
    telnet = None
    
    def __init__(self, fritzbox="192.168.178.1"):
        
        nc = notifier()
        self.connect(fritzbox)
        telnet = self.telnet
        
        logging.info('Connected to Telnet: {0}'.format(str(telnet)))

        while True:
            logging.info('Waiting for nother event')
            
            data = telnet.read_until('POTS;', 300) # maybe read while 1 and then do
            number = '\n'.join(self.only_number.findall(data))
            
            logging.info('The number extracted form: {0} is: {1}'.format(data, number))
            
            if number:
                nc.notify("Incomming call", "From: {0}".format(number))


    def connect(self, fritzbox):
        for i in range(3):
            try:
                self.telnet = Telnet(fritzbox, '1012', 60)
                logging.info('Telnet connection to {0} succseed'.format(fritzbox))
                break
            except:
                message = 'Telnet connection #{0} failed'.format(i)
                if i >= 3:
                    logging.Waiting(message)
                else:
                    logging.info(message)
        return 0





if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='call_monitor.log',level=logging.INFO)
    log = logging.basicConfig()
    callmonitor = voip()

