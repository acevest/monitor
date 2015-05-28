#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: Monitor.py
#      Author: Zhao Yanbai
#              Sun Dec 28 15:38:41 2014
# Description: none
# ------------------------------------------------------------------------
import time
import serial
import os
import commands
import web
import json
import sys
sys.path.append('..')
import config
from utils import *
from mail  import SendMail
from weixin import SendWeiXinMsg

def SendMsg(title, msg) :
    SendMail(title, msg)
    SendWeiXinMsg(msg)

log = CreateLogger(config.ACE_GLOBAL_LOG_PATH)

class dbHandler(DBBase) :
    def __init__(self) :
        super(dbHandler, self).__init__(config.db)

    def Add(self, Light, Temperature) :
        sql = "INSERT INTO SensorValue VALUES(NULL, {0}, {1});".format(Light, Temperature)
        #log.info('SQL:' + sql)
        self.Modify(sql)
        if self.IsFail() :
            log.error('SQL Executed Faild.')

    def Update(self, Light, Temperature, HumanBody) :
        sql = "UPDATE SensorImmediatelyValue SET Time=CURRENT_TIMESTAMP, Light={0}, Temperature={1}, HumanBody={2};".format(Light, Temperature, HumanBody)
        #log.info('SQL:' + sql)
        self.Modify(sql)
        if self.IsFail() :
            log.error('SQL Executed Faild.')


    def Get(self) :
        sql = "SELECT * FROM SensorImmediatelyValue LIMIT 1"
        rs = self.Read(sql)
        try :
            r = rs[0]
        except :
            r = None

        return r

db = dbHandler()


import glob
def ReadSerial(prefix, band) :
    devs = glob.glob(prefix + '*')
    s = None
    for d in devs :
        try :
            print "open ", d
            s = serial.Serial(d, band)
        except Exception, e :
            log.error(str(e))   
            continue
    
    if s == None :
        return

    while True :
        line = s.readline().strip()
        print line
        time.sleep(1)

    s.close()

def main() :
    while True :
        #ReadSerial('/dev/ttyACM', 9600)
        ReadSerial('/dev/rfcomm0', 9600)
        time.sleep(1)

if __name__ == "__main__" :
    main()
