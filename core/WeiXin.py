#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: WeiXin.py
#      Author: Zhao Yanbai
#              Mon Dec 22 22:43:05 2014
# Description: none
# ------------------------------------------------------------------------
import time
import os
import web
import json
import sys
import config
import hashlib
from utils import *

#class WeiXinMgr(PageBase):
class WeiXinMgr(PageBase):
    def GET(self) :
        wi = web.input()
        signature = wi.get('signature')
        timestamp = wi.get('timestamp')
        nonce     = wi.get('nonce')
        echostr   = wi.get('echostr')

        token     = 'token'

        s = "".join(sorted([timestamp, nonce, token]))
        print s
        print hashlib.sha1(s)
        print signature, timestamp, nonce, echostr

        return echostr
