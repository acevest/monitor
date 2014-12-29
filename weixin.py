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
import logging
import ConfigParser

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
    logging.info("request: " + url + " " + data)
    try :
        response = urllib2.urlopen(req, data) 
        rsp = response.read()
        print rsp
        logging.info("response: " + rsp)
        return True
    except :
        pass
    return False


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

        return POST(url, data)

    except Exception, e:  
        logging.error(str(e))

    return False

def SendWeiXinMsg(msg) :
    return SEND_MSG(msg)
