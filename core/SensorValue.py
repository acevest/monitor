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
from utils import *

class dbSensorValue(DBBase) :
    def __init__(self) :
        super(dbSensorValue, self).__init__(config.db)

    def ReadData(self, cnt=288):
        sql = "SELECT * FROM SensorValue ORDER BY Ts DESC LIMIT {0};".format(cnt)
        return self.Read(sql)

db = dbSensorValue()

class SensorValueMgr(PageBase):
    def __init__(self) :
        super(SensorValueMgr, self).__init__()
        self.SetActionHandler('Json',    self.Json)

    def Json(self) :
        rs = db.ReadData()
        rs = rs[::-1]
        for r in rs :
            r.Ts = str(r.Ts)
        return json.dumps(rs, ensure_ascii=False)
        

    def List(self) :
        return config.render.SensorValueList()
