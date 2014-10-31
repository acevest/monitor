#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: config.py
#      Author: Zhao Yanbai
#              Fri Oct 31 05:43:54 2014
# Description: none
# ------------------------------------------------------------------------

import web
from web.contrib.template import render_mako

ACE_GLOBAL_CONF_PATH = '/etc/AceGlobal.conf'
ACE_GLOBAL_LOG_PATH  = '/var/log/AceGlobal.log'

DBHost = '127.0.0.1'
DBName = 'monitor'
DBUser = 'root'
DBPass = 'root'
DBCharset = 'utf8'


db = web.database(      dbn     = 'mysql',
                        host    = DBHost,
                        db      = DBName,
                        user    = DBUser,
                        pw      = DBPass,
                        charset = DBCharset)



render = render_mako(directories=['mako/'], input_encoding='utf-8', output_encoding='utf-8')
