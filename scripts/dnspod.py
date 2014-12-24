#!/usr/bin/env python
#-*- coding:utf-8 -*-

import httplib, urllib
import socket
import time
import sys
import ConfigParser

sys.path.append('..')
import config
from utils import * 

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
current_ip = None

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

def getip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip

if __name__ == '__main__':
    while True:
        try:
            ip = getip()
            print ip
            if current_ip != ip:
                if ddns(ip):
                    current_ip = ip
        except Exception, e:
            print e
            pass
        time.sleep(30)
