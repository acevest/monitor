#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: SerialParser.py
#      Author: Zhao Yanbai
#              Fri Oct 31 08:01:00 2014
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

db = dbHandler()

def main() :
    try :
        s = serial.Serial('/dev/ttyACM0', 9600)
    except Exception, e:
        log.error(str(e))
        return

    while True :
        line = s.readline().strip()
        if line[0] == '>' :
            break

    values = line[1:].strip().split(':')

    try :
        Light = values[0]
        Temperature = values[1]
        db.Add(Light, Temperature)
    except Exception, e :
        log.error(str(e))   
    

if __name__ == "__main__" :
    main()
