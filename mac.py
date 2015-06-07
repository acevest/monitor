#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: mac.py
#      Author: Zhao Yanbai
#              Thu May 28 16:43:33 2015
# Description: none
# ------------------------------------------------------------------------

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scapy.all import srp,Ether,ARP,conf
ipscan='192.168.1.0/24'
try:
    ans,unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ipscan), iface='wlan0', timeout=9, verbose=False)
except Exception,e:
    print str(e)
else:
    for snd,rcv in ans:
        list_mac=rcv.sprintf("%Ether.src% - %ARP.psrc%")
        print list_mac


