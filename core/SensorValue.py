#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: SensorValue.py
#      Author: Zhao Yanbai
#              Fri Oct 31 14:42:42 2014
# Description: none
# ------------------------------------------------------------------------

import time
import os
import web
import json
import sys
import config
import commands
import serial
from utils import *

class dbSensorValue(DBBase) :
    def __init__(self) :
        super(dbSensorValue, self).__init__(config.db)

    def ReadData(self, cnt=288):
        sql = "SELECT * FROM SensorValue ORDER BY Ts DESC LIMIT {0};".format(cnt)
        return self.Read(sql)

    def ReadImmediatelyData(self) :
        sql = "SELECT * FROM SensorImmediatelyValue LIMIT 1;"
        return self.Read(sql)

db = dbSensorValue()

class SensorValueMgr(PageBase):
    def __init__(self) :
        super(SensorValueMgr, self).__init__()
        self.SetActionHandler('Json',    self.Json)
        self.SetActionHandler('ImmediatelyList',    self.ImmediatelyList)
        self.SetActionHandler('ImmediatelyJson',    self.ImmediatelyJson)

    def Json(self) :
        rs = db.ReadData()
        rs = rs[::-1]
        for r in rs :
            r.Ts = str(r.Ts)
        return json.dumps(rs, ensure_ascii=False)
        

    def List(self) :
        return config.render.SensorValueList()


    def ImmediatelyList(self) :
        return config.render.SensorValueImmediatelyList()

    def ImmediatelyJson(self) :
        rs = db.ReadImmediatelyData()
        try :
            r = rs[0]
            Light = r.Light
            Temperature = r.Temperature
        except :
            Light = 0
            Temperature = 0.0
        data = { 'Ts' : Ts2TmStr(int(time.time())), 'Light' : Light, 'Temperature' : Temperature }
        return self.SucJsonData(data)
