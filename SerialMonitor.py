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
import logging
import config
from utils import *

init_logging(config.ACE_GLOBAL_LOG_PATH)
class dbHandler(DBBase) :
    def __init__(self) :
        super(dbHandler, self).__init__(config.db)

    def Add(self, Light, Temperature, HumanBody) :
        sql = "INSERT INTO SensorValue VALUES(NULL, {0}, {1}, {2});".format(Light, Temperature, HumanBody)
        #logging.info('SQL:' + sql)
        self.Modify(sql)
        if self.IsFail() :
            logging.error('SQL Executed Faild.')

    def Update(self, Light, Temperature, HumanBody) :
        sql = "UPDATE SensorImmediatelyValue SET Time=CURRENT_TIMESTAMP, Light={0}, Temperature={1}, HumanBody={2};".format(Light, Temperature, HumanBody)
        #logging.info('SQL:' + sql)
        self.Modify(sql)
        if self.IsFail() :
            logging.error('SQL Executed Faild.')


    def Get(self) :
        sql = "SELECT * FROM SensorImmediatelyValue LIMIT 1"
        rs = self.Read(sql)
        try :
            r = rs[0]
        except :
            r = None

        return r

db = dbHandler()

import RPi.GPIO as GPIO
class PiMgr(Storage) :
    def __init__(self) :
        super(PiMgr, self).__init__()
        self.LedPin = 7
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LedPin, GPIO.OUT)
        self.LedTimeout = 30
        self.LedTurnOnTs = 0

    def TurnLedOn(self) :
        GPIO.output(self.LedPin, GPIO.HIGH)
        self.LedTurnOnTs = int(time.time())

    def TurnLedOff(self) :
        if int(time.time()) - self.LedTurnOnTs > self.LedTimeout :
            GPIO.output(self.LedPin, GPIO.LOW)

pimgr = PiMgr()

def main() :
    LastInsert = 0
    while True :
        try :
            s = serial.Serial('/dev/ttyACM0', 9600)
            while True :
                line = s.readline().strip()
                print line
                if line[0] == '>' :
                    break

            values = line[1:].strip().split(':')

            Light = float(values[0])
            Temperature = float(values[1])
            HumanBody = int(values[2])

            r = db.Get()
            if None != r :
                OldLight        = float(r.Light)
                OldHumanBody    = int(r.HumanBody)
                print("Light {0} OldLight {1} HumanBody {2} OldHumanBody {3}".format(Light, OldLight, HumanBody, OldHumanBody))
                if (OldLight < 290 and Light > 340) or (Light - OldLight > 50) :
                    logging.info("Light was Turned On Light {0} OldLight {1}".format(Light, OldLight))
                    if int(r.Switch) == 1 :
                        SendMsg("Light was Turned On", "Light {0} OldLight {1}".format(Light, OldLight))

                if HumanBody > 0 :
                    logging.info("HumanBody {0} OldHumanBody {1}".format(HumanBody, OldHumanBody))

                if OldHumanBody == 0 and HumanBody > 10 :
                    logging.info("Someone Accessed. HumanBody {0} OldHumanBody {1}".format(HumanBody, OldHumanBody))
                    if int(r.Switch) == 1 :
                        SendMsg("Someone Accessed", "HumanBody {0} OldHumanBody {1}".format(HumanBody, OldHumanBody))

            db.Update(Light, Temperature, HumanBody)

            n = int(time.time()) / 60
            if n > LastInsert :
                LastInsert = n
                db.Add(Light, Temperature, HumanBody)

            if HumanBody > 0 :
                pimgr.TurnLedOn()

            pimgr.TurnLedOff()
        except Exception, e :
            logging.error(str(e))   
            time.sleep(1)
            continue
    

if __name__ == "__main__" :
    main()
