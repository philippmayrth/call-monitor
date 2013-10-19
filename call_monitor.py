#!/usr/bin/env python

"""
    State controll keys for your fritz.box voipAPI:
        Activate: #96*5*
        Dissable: #96*4*
"""

import os
import re
import logging
from telnetlib import Telnet

pathNotificationApp = "./core/terminal-notifier.app/Contents/MacOS/terminal-notifier"

class notifier:
    def notify(self, title="call monitor", message="a event occured"):
        shell = ' -title "{0}" -message "{1}"'.format(title, message)
        assambled = pathNotificationApp + shell
        os.system(assambled)



class voip:
    only_number = re.compile('.*RING;\d*;(\d*);.*')
    
    def __init__(self, fritzbox="192.168.178.1"):
        
        nc = notifier()

        telnet = Telnet(fritzbox, '1012')
        
        print "i: connected to telnet: " + str(telnet)

        while True:
            print "read telnet date til POTS;"
            data = telnet.read_until('POTS;', 300) # maybe read while 1 and then do (if 'RING' in s) ..
            print "extract number from this data: " + data
            number = '\n'.join(self.only_number.findall(data))
            
            print "the number is: " + str(number)

            if number:
                print "notify"
                nc.notify("Incomming call", "From: {0}".format(number))



if __name__ == "__main__":
    log = logging.basicConfig()
    callmonitor = voip()
