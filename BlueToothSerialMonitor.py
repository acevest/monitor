#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: BlueToothSerialMonitor.py
#      Author: Zhao Yanbai
#              Fri May 29 16:10:31 2015
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


def main() :
    s = serial.Serial('/dev/rfcomm0', 9600)


if __name__ == "__main__" :
    pass
