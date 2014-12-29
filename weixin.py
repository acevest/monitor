#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: weixin.py
#      Author: Zhao Yanbai
#              Sun Dec 28 14:09:13 2014
# Description: none
# ------------------------------------------------------------------------
import json
import config
import urllib
import urllib2
import ConfigParser
from utils import * 

def GET_TOKEN(corpid, corpsecret) :
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}".format(corpid, corpsecret)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return json.loads(response.read())["access_token"]

def POST(url, data) :
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    data = json.dumps(data, ensure_ascii=False)
    print data
    response = urllib2.urlopen(req, data) 
    return response.read()


def SEND_MSG(msg) :
    cnfp = ConfigParser.ConfigParser()
    cnfp.read(config.ACE_GLOBAL_CONF_PATH)
    corpid      = cnfp.get('WEIXIN', 'CORPID')
    corpsecret  = cnfp.get('WEIXIN', 'CORPSECRET')

    try :
        token = GET_TOKEN(corpid, corpsecret)
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={0}".format(token)

        data = {
            "touser" : "@all",
            "msgtype" : "text",
            "agentid" : "0",
            "text" : {
                "content" : msg
            },
            "safe" : "0"
        }

        POST(url, data)

    except Exception, e:  
        log = CreateLogger(config.ACE_GLOBAL_LOG_PATH)
        log.error(str(e))

def SendWeiXinMsg(msg) :
    SEND_MSG(msg)
