#!/usr/bin/env python

"""
    License:    CC 4.0 --> BY - NC - SA
                For more info see creativecommons.org
                All right
    
	Notifications require OS X v10.9
	
    State controll keys for your fritz.box voipAPI:
        Activate: #96*5*
        Dissable: #96*4*
"""

import os
import re
import logging
import signal
from telnetlib import Telnet


class notifier:
    def notify(self, title="call monitor", message="a event occured"):
        assambled = 'osascript -e \'display notification \"{0}\" with title \"{1}\"\''.format(message, title)
        logging.info('Assambled comand for notification: {0}'.format(assambled))
        os.system(assambled)


class voip:
    only_number = re.compile('.*RING;\d*;(\d*);.*')
    fritzbox = None
    telnet = None
    
    def __init__(self, fritzbox="192.168.178.1"):
        
        self.fritzbox = fritzbox
        
        nc = notifier()
        self.connect()
        telnet = self.telnet
        
        logging.info('Connected to Telnet: {0}'.format(str(telnet)))

        while True:
            try:
                logging.info('Waiting for nother event')
            
                try:
                    data = telnet.read_until('POTS;', 300) # maybe read while 1 and then do
                except EOFError:
                    logging.Waiting('Lost connection to telnet server')
                    self.reconnect()
                
                
                number = '\n'.join(self.only_number.findall(data))
            
                logging.info('The number extracted form: {0} is: {1}'.format(data, number))
            
                if number:
                    nc.notify("Incomming call", "From: {0}".format(number))
            except KeyboardInterrupt:
                    logging.info('KeyboardInterrupt')
                    self.delete()
                    exit()


    def connect(self):
        fritzbox = self.fritzbox
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

    def reconnect(self):
        self.telnet.close()
        self.connect()

    def delete(self):
        logging.info('Clearing Telnet session up')
        self.telnet.close()



if __name__ == "__main__":

    def onExit():
        logging.info('exiting')
        callmonitor.delete()
        exit()


    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='call_monitor.log',level=logging.INFO)
    log = logging.basicConfig()
    
    signal.signal(signal.SIGTERM, onExit)
    callmonitor = voip()

