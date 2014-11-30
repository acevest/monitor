#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: SerialMonitor.py
#      Author: Zhao Yanbai
#              Sun Nov  2 17:18:30 2014
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

    def Update(self, Light, Temperature) :
        sql = "UPDATE SensorImmediatelyValue SET Ts=CURRENT_TIMESTAMP, Light={0}, Temperature={1};".format(Light, Temperature)
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

def main() :
    LastInsert = 0
    while True :
        try :
            try :
                s = serial.Serial('/dev/ttyACM0', 9600)
            except Exception, e :
                time.sleep(1)
                log.error(str(e))   
                continue

            while True :
                line = s.readline().strip()
                if line[0] == '>' :
                    break

            values = line[1:].strip().split(':')

            Light = float(values[0])
            Temperature = float(values[1])

            r = db.Get()
            if None != r :
                OldLight = float(r.Light)
                print("Light Light {0} OldLight {1}".format(Light, OldLight))
                if (OldLight < 290 and Light > 340) or (Light - OldLight > 50) :
                    log.info("Light was Turned On Light {0} OldLight {1}".format(Light, OldLight))
                    SendMail("Light was Turned On", "Light {0} OldLight {1}".format(Light, OldLight))

            db.Update(Light, Temperature)

            n = int(time.time()) / 60
            if n > LastInsert :
                LastInsert = n
                db.Add(Light, Temperature)

        except Exception, e :
            log.error(str(e))   
            continue
    

if __name__ == "__main__" :
    main()
