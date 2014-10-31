#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: main.py
#      Author: Zhao Yanbai
#              Fri Oct 31 05:43:35 2014
# Description: 
#       #nohup python main.py 36000 >/dev/null 2>&1 &
# ------------------------------------------------------------------------

import web
import urls
import config
from utils import *

class Failed:
    def GET(self) :
        return u"Failed...."

class ErrMsg :
    def GET(self) :
        msg = web.input().get('msg', u'No Error Message')
        return msg

class Index :
    def GET(self) :
        return config.render.Index()
    def POST(self) :
        return config.render.Index()

app = web.application(urls.urls, globals())

if __name__ == "__main__" :
    try :
        app.run()

    except BaseException :
        import traceback
        print traceback.format_exc()
