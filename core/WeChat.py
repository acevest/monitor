#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: WeChat.py
#      Author: Zhao Yanbai
#              Wed Jan 14 14:36:33 2015
# Description: none
# ------------------------------------------------------------------------
import web
import json
import hashlib
import xml.etree.cElementTree as ET
import logging
import ConfigParser
from utils import *
import config
from WXBizMsgCrypt import WXBizMsgCrypt


class WeChatMgr(PageBase):
    def __init__(self) :
        super(WeChatMgr, self).__init__()


    def DoCmd(self, Cmd) :
        cmd = Cmd.strip()
        argv= [arg.strip() for arg in cmd.split()]
        if len(argv) == 0 or argv[0] not in ['help'] :
            return u'不支持该命令, 详情请参考help'

        if argv[0] == 'help' :
            return u'NO HELP.\n'

        return u'''暂不支持'''


    def List(self) :
        cnfp = ConfigParser.ConfigParser()
        cnfp.read(config.ACE_GLOBAL_CONF_PATH)
        Token           = cnfp.get('WEIXIN', 'Token') 
        EncodingAESKey  = cnfp.get('WEIXIN', 'EncodingAESKey')
        CorpID          = cnfp.get('WEIXIN', 'CORPID')

        print Token, EncodingAESKey, CorpID

        wxcpt = WXBizMsgCrypt(Token,EncodingAESKey,CorpID)

        wi = web.input()
        sReqMsgSig = wi.get('msg_signature')
        sReqTimeStamp = wi.get('timestamp')
        sReqNonce = wi.get('nonce')
        sReqData = web.data()


        '''
        # 仅验证时用
        sEchoStr = wi.get('echostr')
        ret, EchoStr = wxcpt.VerifyURL(sReqMsgSig, sReqTimeStamp, sReqNonce, sEchoStr)
        if(ret != 0) :
            print "ERR: VerifyURL ret: ", ret
            return

        return EchoStr 
        '''

        print sReqMsgSig, sReqTimeStamp, sReqNonce, sReqData
        ret,sMsg=wxcpt.DecryptMsg( sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        if( ret!=0 ):
            print "ERR: DecryptMsg ret: ", ret
            return
          
        # 解密成功，sMsg即为xml格式的明文
        xml_tree = ET.fromstring(sMsg)
        Content = xml_tree.find("Content").text
        ToUserName = xml_tree.find("ToUserName").text
        FromUserName = xml_tree.find("FromUserName").text
        MsgId = xml_tree.find("MsgId").text


        Content = self.DoCmd(Content)

        print xml_tree
        #print "RECEIVED DATA: ", Content, ToUserName, FromUserName, MsgId

        sRespData = """
            <xml>
            <ToUserName><![CDATA[{0}]]></ToUserName>
            <FromUserName><![CDATA[{1}]]></FromUserName>
            <CreateTime>{2}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{3}]]></Content>
            <MsgId>{4}</MsgId>
            <AgentID>2</AgentID>
            </xml>
        """.format(FromUserName, ToUserName, int(time.time()), Content, MsgId)

        #print sRespData
        ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, sReqNonce, sReqTimeStamp)
        if( ret!=0 ):
            print "ERR: EncryptMsg ret: " + ret
            return

        return sEncryptMsg

