#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: GetWanIP.py
#      Author: Zhao Yanbai
#              Thu Oct 30 04:34:37 2014
# Description: none
# ------------------------------------------------------------------------
import httplib, urllib
import socket
import time
import sys
import os
import re,urllib2
import smtplib  
import ConfigParser
from email.mime.text import MIMEText  
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


cnfp = ConfigParser.ConfigParser()
cnfp.read(config.ACE_GLOBAL_CONF_PATH)
params = dict(
    login_email     = cnfp.get('DNSPOD', 'EMAIL'),
    login_password  = cnfp.get('DNSPOD', 'PASSWD'),
    format="json",
    domain_id       = cnfp.get('DNSPOD', 'DOMAINID'),
    record_id       = cnfp.get('DNSPOD', 'RECORDID'),
    sub_domain="",
    record_line="默认",
)

def ddns(ip):
    params.update(dict(value=ip))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.Ddns", urllib.urlencode(params), headers)
    
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    conn.close()
    return response.status == 200

if __name__ == '__main__':  
    WanIP = GetWanIP().GetIP()
    if not "".join(WanIP.split(".")).isdigit() :
        log.error("Invalid IP Address {0}".format(WanIP))
        sys.exit(0)
    try :
        fd = open(TMP_FILE_PATH)
        OldWanIP = fd.readline().strip()
        fd.close()
    except :
        OldWanIP = '0.0.0.0'

    if OldWanIP != WanIP :
        s = 'WanIP has Changed From ' + OldWanIP + ' To ' + WanIP

        if ddns(WanIP) :
            fd = open(TMP_FILE_PATH, 'w+')
            fd.write(WanIP+'\n')
            fd.close()
        else :
            s += u' 但是DDNS是失败'

        log.info(s)
        SendMsg(u'外网IP有变动', s)
