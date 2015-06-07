#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: b.py
#      Author: Zhao Yanbai
#              Thu May 28 16:06:28 2015
# Description: none
# ------------------------------------------------------------------------
import os,socket
LanIPList = os.popen("ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | sed 's/addr://g'").readlines()
try :
    for LanIP in LanIPList :
        LanIPPrefix = ".".join(LanIP.split(".")[:3])
        print LanIPPrefix
        for i in range(1, 255) :
            try :
                ip = LanIPPrefix + "." + str(i)
                print ip
                print '\t'+ip+'\t======>\t'+socket.gethostbyaddr(ip)[0]
            except :
                pass
except :
    LanIP = 'NoLanIP'
    print "Error: Can not Find Lan IP" 
