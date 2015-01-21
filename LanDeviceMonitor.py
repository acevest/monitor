#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: LanDeviceMonitor.py
#      Author: Zhao Yanbai
#              Mon Dec 29 20:25:56 2014
# Description: none
# ------------------------------------------------------------------------
import os
import sys
import commands
import logging
import config
from utils import *

init_logging(config.ACE_GLOBAL_LOG_PATH)

class dbHandler(DBBase) :
    def __init__(self) :
        super(dbHandler, self).__init__(config.db)

    def Add(self, mac) :
        sql = "INSERT INTO Devices(MacAddr, Name, State, Ts, Notify) VALUES('{0}', 'Unknown', 1, CURRENT_TIMESTAMP, 1);".format(mac)
        logging.info('SQL:' + sql)
        self.Modify(sql)
        if self.IsFail() :
            logging.error('SQL Executed Faild.')

    def Update(self, mac, state) :
        sql = "UPDATE Devices SET Ts=CURRENT_TIMESTAMP, State={1} where MacAddr='{0}'".format(mac, state)
        logging.info('SQL:' + sql)
        self.Modify(sql)
        if self.IsFail() :
            logging.error('SQL Executed Faild.')


    def Get(self) :
        sql = "SELECT * FROM Devices"
        return self.Read(sql)

    def BuildMacListStr(self, macs) :
        rs = self.Get()
        s = ''
        for r in rs :
            if r.MacAddr in macs :
                s += '['
                s += r.Name
                s += ':'
                s += r.MacAddr
                s += ']'

        return s

db = dbHandler()

def ScanMacs() :
    cmd = """nmap -PR 192.168.1.1/24 | grep "MAC Address" | awk '{print $3}'"""
    out = commands.getoutput(cmd)

    macs = set()
    for mac in out.splitlines() :
        s = "".join(mac.split(':'))
        try :
            n = int(s, 16)
        except :
            continue

        macs.add(mac)


    return macs


def main() :
    macs = ScanMacs()
    print macs

    macrs = db.Get()
    dbmacs = set()

    NewMac          = set()
    Switch2AliveMac = set()
    Switch2DeadMac  = set()


    for r in macrs :
        if r.Notify == 0 :
            try :
                macs.remove(r.MacAddr)
            except :
                pass
            continue

    for r in macrs :
        dbmacs.add(r.MacAddr)

        r.State = int(r.State)

        # Switch to ALIVE
        if r.State == 0 and r.MacAddr in macs :
            Switch2AliveMac.add(r.MacAddr)
            db.Update(r.MacAddr, 1)
        elif r.State == 1 and r.MacAddr not in macs :
            Switch2DeadMac.add(r.MacAddr)
            db.Update(r.MacAddr, 0)

    for mac in macs :
        if mac not in dbmacs :
            NewMac.add(mac)
            db.Add(mac)

    msg = u''
    if len(NewMac) != 0 :
        msg += u' New Device: '
        msg += db.BuildMacListStr(NewMac)
        msg += ';'

    if len(Switch2AliveMac) != 0 :
        msg += u' Switch to Alive Device: '
        msg += db.BuildMacListStr(Switch2AliveMac)
        msg += ';'

    if len(Switch2DeadMac) != 0 :
        msg += u' Switch to Dead Device: '
        msg += db.BuildMacListStr(Switch2DeadMac)
        msg += ';'

    if len(msg) != 0 :
        logging.info(msg)
        SendMsg('Mac Monitor', msg)

if __name__ == "__main__" :
        main()
