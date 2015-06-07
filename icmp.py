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
    ans,unans=sr(IP(dst="192.168.1.1-254")/ICMP())
except Exception,e:
    print str(e)
else:
    ans.summary(lambda (s,r): r.sprintf("%IP.src% is alive") )


