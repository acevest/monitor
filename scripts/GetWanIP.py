#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: GetWanIP.py
#      Author: Zhao Yanbai
#              Thu Oct 30 04:34:37 2014
# Description: none
# ------------------------------------------------------------------------
import os
import sys
import re,urllib2
import smtplib  
import ConfigParser
from email.mime.text import MIMEText  
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append('..')
import config
from utils import * 
from mail  import SendMail
from weixin import SendWeiXinMsg

def SendMsg(title, msg) :
    SendMail(title, msg)
    SendWeiXinMsg(msg)

TMP_FILE_PATH = '/tmp/GetWanIP.txt'
log = CreateLogger(config.ACE_GLOBAL_LOG_PATH)
  
class GetWanIP:
    def GetIP(self):
        try:
            log.info('Try ip.qq.com')
            WanIP = self.Visit('http://ip.qq.com')
        except:
            s = 'Failed to Get WanIP!!!'
            WanIP = s
            log.error(s)
        return WanIP

    def Visit(self,url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)


if __name__ == '__main__':  
    try :
        fd = open(TMP_FILE_PATH)
        OldWanIP = fd.readline().strip()
        fd.close()
    except :
        OldWanIP = '0.0.0.0'

    WanIP = GetWanIP().GetIP()

    if OldWanIP != WanIP :
        s = 'WanIP has Changed From ' + OldWanIP + ' To ' + WanIP
        log.info(s)
        SendMsg(u'外网IP有变动', s)
        fd = open(TMP_FILE_PATH, 'w+')
        fd.write(WanIP+'\n')
        fd.close()
