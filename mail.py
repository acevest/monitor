#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#   File Name: mail.py
#      Author: Zhao Yanbai
#              Thu Nov  6 07:23:46 2014
# Description: none
# ------------------------------------------------------------------------

import os
import sys
import re,urllib2
import smtplib  
import ConfigParser
from email.mime.text import MIMEText  
import config
from utils import * 

  
def send_mail(to_list, mail_host, mail_user, user_nick, mail_pass, mail_postfix, sub, content) :
    #def send_mail(to_list,sub,content):                                 #to_list：收件人；sub：主题；content：邮件内容
    me=user_nick+"<"+mail_user+"@"+mail_postfix+">"                 #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='gb2312')       #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub                #设置主题
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    s = smtplib.SMTP()  
    print mail_host
    s.connect(mail_host)                        #连接smtp服务器
    s.login(mail_user,mail_pass)                #登陆服务器
    s.sendmail(me, to_list, msg.as_string())    #发送邮件
    s.close()  

def SendMail(title, msg) :
    log = CreateLogger(config.ACE_GLOBAL_LOG_PATH)
    cnfp = ConfigParser.ConfigParser()
    cnfp.read(config.ACE_GLOBAL_CONF_PATH)
    mailto_list = []
    mailto_list.append(cnfp.get('EMAIL', 'MAILTO'))
    mail_host = cnfp.get('EMAIL', 'MAILHOST')
    mail_user = cnfp.get('EMAIL', 'MAILUSER')
    user_nick = cnfp.get('EMAIL', 'USERNICK')
    mail_pass = cnfp.get('EMAIL', 'MAILPASS')
    mail_postfix = cnfp.get('EMAIL', 'MAILPOSTFIX')


    try :
        print mailto_list, mail_host,mail_user, user_nick, mail_pass, mail_postfix
        send_mail(mailto_list,mail_host, mail_user, user_nick, mail_pass, mail_postfix, title, msg)
        log.info('发送成功')
        return True
    except Exception, e:  
        log.error(str(e))
        log.error('发送失败')
        return False

    return False
