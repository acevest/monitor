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

    def ReadData(self, cnt=1000, days=1):
        sql = "SELECT * FROM SensorValue WHERE UNIX_TIMESTAMP(Ts) mod {0} = 0 ORDER BY Ts DESC LIMIT {1};".format(cnt, days*60)
        return self.Read(sql)

    def ReadImmediatelyData(self) :
        sql = "SELECT * FROM SensorImmediatelyValue LIMIT 1;"
        return self.Read(sql)

    def Switch(self, value) :
        sql = "UPDATE SensorImmediatelyValue SET Switch={0}".format(value)
        self.Modify(sql)
        return self.Ret()

db = dbSensorValue()

class SensorValueMgr(PageBase):
    def __init__(self) :
        super(SensorValueMgr, self).__init__()
        self.SetActionHandler('Json',    self.Json)
        self.SetActionHandler('Switch',  self.Switch)
        self.SetActionHandler('ImmediatelyList',    self.ImmediatelyList)
        self.SetActionHandler('ImmediatelyJson',    self.ImmediatelyJson)
    def Switch(self) :
        Value = web.input().get('Value', 1)
        return db.Switch(Value)
        

    def Json(self) :
        try :
            days = int(web.input().get('Days', 1))
        except :
            days = 1
        rs = db.ReadData(1000, days)
        rs = rs[::-1]
        for r in rs :
            r.Ts = str(r.Ts)
        return json.dumps(rs, ensure_ascii=False)
        

    def List(self) :
        return config.render.SensorValueList()


    def ImmediatelyList(self) :
        rs = db.ReadImmediatelyData()
        return config.render.SensorValueImmediatelyList(Cfg=rs[0])

    def ImmediatelyJson(self) :
        rs = db.ReadImmediatelyData()
        try :
            r = rs[0]
        except :
            pass # return Err

        r.Time = Ts2TmStr(int(time.time()))
        return self.SucJsonData(r)
