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

log = CreateLogger(config.ACE_GLOBAL_LOG_PATH)

class dbHandler(DBBase) :
    def __init__(self) :
        super(dbHandler, self).__init__(config.db)

    def Add(self, Light, Temperature) :
        sql = "INSERT INTO SensorValue VALUES(NULL, {0}, {1});".format(Light, Temperature)
        log.info('SQL:' + sql)
        self.Modify(sql)
        if self.IsFail() :
            log.error('SQL Executed Faild.')

    def Update(self, Light, Temperature) :
        sql = "UPDATE SensorImmediatelyValue SET Ts=CURRENT_TIMESTAMP, Light={0}, Temperature={1};".format(Light, Temperature)
        log.info('SQL:' + sql)
        self.Modify(sql)
        if self.IsFail() :
            log.error('SQL Executed Faild.')

db = dbHandler()

def main() :
    LastInsert = 0
    while True :
        try :
            s = serial.Serial('/dev/ttyACM0', 9600)

            while True :
                line = s.readline().strip()
                if line[0] == '>' :
                    break

            values = line[1:].strip().split(':')

            Light = values[0]
            Temperature = values[1]
            
            n = int(time.time()) / 600
            if n > LastInsert :
                LastInsert = n
                db.Add(Light, Temperature)

            db.Update(Light, Temperature)
        except Exception, e :
            log.error(str(e))   
            continue
    

if __name__ == "__main__" :
    main()
