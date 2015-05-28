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
s = serial.Serial('/dev/rfcomm0', 9600)
while True :
    line = s.readline().strip()
    print line
    time.sleep(0.1)
