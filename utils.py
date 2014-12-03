#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: utils.py
#      Author: Zhao Yanbai
#              Thu Oct 30 06:33:24 2014
# Description: none
# ------------------------------------------------------------------------

import logging
import struct
import socket
import web
import MySQLdb
import commands
import json
import time


def CreateLogger(logpath, level=logging.DEBUG)  :
    logger  = logging.getLogger(logpath)
    fmtr    = logging.Formatter('%(levelname)s\t%(asctime)s: %(message)s')

    fileHdlr    = logging.FileHandler(logpath)
    fileHdlr.setFormatter(fmtr)
    fileHdlr.setLevel(level)

    streamHdlr  = logging.StreamHandler()
    streamHdlr.setFormatter(fmtr)
    streamHdlr.setLevel(level)

    logger.addHandler(fileHdlr)
    logger.addHandler(streamHdlr)
    logger.setLevel(level)

    return logger

class Storage(dict) :
    def __getattr__(self, key) :
        try :
            return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value) :
        self[key] = value

    def __delattr__(self, key) :
        try :
            del self[key]
        except KeyError, k:
            raise AttributeError, k

    def __repr__(self) :
        return '<Storage ' + dict.__repr__(self) + '>'

def ip2int(ip) :
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def int2ip(i) :
    print i
    return str(socket.inet_ntoa(struct.pack("!I", int(i))))


def INET_ATON(ipstr) :
    ip = ip2int(ipstr)
    return str(ip)

def INET_NTOA(ip) :
    ipstr = int2ip(int(ip) & 0xFFFFFFFF)
    return ipstr

def CheckIP(s) :
    try :
        return len([i for i in s.split('.') if (0<= int(i)<= 255)])== 4
    except :
        return False

def CheckPort(port) :
    return port.isdigit() and int(port) > 0 and int(port) < 65536 

def CheckLogic(logic) :
    if not logic.isdigit() :
        return False
    logic = int(logic)
    return (logic == 0 or logic == 1 or logic == 2)


class PageBase(object):
    def __init__(self) :
        self.ActionMap = { }
        self.action = ''
        self.SetActionHandler('New',    self.New)
        self.SetActionHandler('Add',    self.Add)
        self.SetActionHandler('Del',    self.Del)
        self.SetActionHandler('Edit',   self.Edit)
        self.SetActionHandler('List',   self.List)
        self.SetActionHandler('Search', self.Search)
        self.SetActionHandler('UNIMPLEMENTED',  self.UNIMPLEMENTED)

        self.Ret = {
            'Err' : -1,
            'Msg' : 'Unknown'
        }

    def ErrMsg(self, msg) :
        self.Ret['Err'] = 1
        self.Ret['Msg'] = msg
        return json.dumps(self.Ret, ensure_ascii=False)
        return self.Ret

    def SucMsg(self, msg) :
        self.Ret['Err'] = 0
        self.Ret['Msg'] = msg
        return json.dumps(self.Ret, ensure_ascii=False)
        return self.Ret

    def SucJsonData(self, data) :
        self.Ret['Err'] = 0
        self.Ret['Msg'] = 'success'
        self.Ret['Data'] = data
        r = json.dumps(self.Ret, ensure_ascii=False)
        return r

    def AuthorizedUser(self) :
        return True

    def UNIMPLEMENTED(self) :
        if len(self.action) == 0 :
            return "UNIMPLEMENTED"
        return "UNIMPLEMENTED HANDLER FOR THE ACTION: {0}".format(self.action)

    def REQUEST_HANDLER(self) :
        self.action = web.input().get('action', '').strip()
        return self.ActionMap.get(self.action, self.UNIMPLEMENTED)()

    def GET(self) :
        if not self.AuthorizedUser() :
            return "UNAUTHORIZED USER"
        return self.REQUEST_HANDLER()

    def POST(self) :
        if not self.AuthorizedUser() :
            return "UNAUTHORIZED USER"
        return self.REQUEST_HANDLER()

    def SetActionHandler(self, action, handler) :
        self.ActionMap[action] = handler

    def New(self) :
        return "YOU MUST IMPLEMENTED HANDLER FOR THE ACTION: {0}".format(self.action)
    def Add(self) :
        return "YOU MUST IMPLEMENTED HANDLER FOR THE ACTION: {0}".format(self.action)
    def Del(self) :
        return "YOU MUST IMPLEMENTED HANDLER FOR THE ACTION: {0}".format(self.action)
    def Edit(self) :
        return "YOU MUST IMPLEMENTED HANDLER FOR THE ACTION: {0}".format(self.action)
    def List(self) :
        return "YOU MUST IMPLEMENTED HANDLER FOR THE ACTION: {0}".format(self.action)
    def Update(self) :
        return "YOU MUST IMPLEMENTED HANDLER FOR THE ACTION: {0}".format(self.action)
    def Search(self) :
        return "YOU MUST IMPLEMENTED HANDLER FOR THE ACTION: {0}".format(self.action)

class DBBase(object):
    def __init__(self, db) :
        self.db = db
        self.ret = {
            "Err" : 0,
            "Msg" : "No Error",
        }

    def SetSuccMsg(self, msg) :
        self.ret["Err"] = 0
        self.ret["Msg"] = msg

    def SetFailMsg(self, msg) :
        self.ret["Err"] = 1
        self.ret["Msg"] = msg

    def IsFail(self) :
        return self.ret['Err'] == 1

    def Fail(self, msg='UnSetErrReason') :
        self.ret['Err'] = 1
        self.ret['Msg'] = msg
        return self.ret

    def Ret(self) :
        return self.ret

    def GetRetMsg(self) :
        return self.ret['Msg']

    def Result(self, url='') :
        if self.IsFail() :
            return self.GetRetMsg()
            #return config.render.ErrMsg(msg=self.GetRetMsg())
        else :
            #return config.render.Msg(msg=self.GetRetMsg(), url = url)
            web.seeother(url)

    def Read(self, sql, sidx="", sord="") :
        if sidx != "" :
            sord = sord.upper()
            if sord != "ASC" and sord != "DESC" :
                sord = "ASC"

            sql = sql + " ORDER BY " + sidx + " " + sord

        try :
            #print sql
            records = list(self.db.query(sql))
        except MySQLdb.ProgrammingError :
            records = []
    
        return records

    def Modify(self, sql) :
        sqls = sql.split(';')
        for sql in sqls :
            if len(sql) < 5 :
                break

            #self.db.query(sql)
            #return
            try :
                #print sql
                self.db.query(sql)
                self.SetSuccMsg(u"操作完成")
            except MySQLdb.ProgrammingError :
                self.SetFailMsg("MySQL Programming Error")
            except MySQLdb.IntegrityError :
                self.SetFailMsg("Duplicate Record")
            except :
                self.SetFailMsg("Unknown Error")

            if self.IsFail() :
                break

        return self.ret

def GetSvrOutputLines(cmd) :
    lines = []
    o = commands.getoutput(cmd)
    #print o
    for line in o.splitlines() :
        if len(line) == 0 :
            break
        if line[0] != '>' :
            continue

        line = line[1:]
        line = line.strip()
        lines.append(line)

    return lines


def Ts2TmStr(ts=int(time.time())) :
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
