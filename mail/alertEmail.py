#! /usr/bin/env python
# -*- coding:utf-8 -*-
#usage: python alertEmail.py alertContent appVersion buildVersion

import sys
import os
import smtplib
import getpass
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

#####################
#   需要配置的参数     #
#####################
# 接受新包邮件的邮箱地址写在alertMailList.txt里面
mailListFile = 'alertMailList.txt'
# 发送邮件的邮箱地址
dailyBuildMailUserName = "TODO"
# 发送邮件的邮箱密码
dailyBuildMailPassword = "TODO"
# 发送邮件邮箱的smtp服务器地址
smtpAddress = "TODO"
# 团队成员的电脑登录名到姓名的映射
author_dict = {
'youmingtaizi':'周春波', 
'wanghui':'汪辉', 
'YG':'崔永国', 
'ethank':'刘东洋', 
'ethankqa':'MacMini'}

# 从package脚本传过来的参数
scheme = sys.argv[1]
alertContent = sys.argv[2]
appVersion = sys.argv[3]
buildVersion = sys.argv[4]
debugOrRelease = sys.argv[5]
chineseName = sys.argv[6]
subject = '【打包失败】' + chineseName

def sendEmail(msgFrom, msgTo):
    msg = MIMEMultipart()
    msg['From'] = msgFrom
    msg['To'] = ','.join(msgTo)
    msg['Subject'] = subject

    # add content
    content = '《' + chineseName + '》' + '版本：' + scheme + '_' + appVersion + '_' + buildVersion + '_' + debugOrRelease + '.app\n'
    content += '操作失败: ' + alertContent
    content += '\n\nAuthor: '
    content += author_dict[getpass.getuser()]
    content += '\n\n'

    txt = MIMEText(content, 'plain', 'utf-8')
    msg.attach(txt)

    # send email
    smtp = smtplib.SMTP(smtpAddress)
    smtp.set_debuglevel(1)
    smtp.ehlo()
    smtp.login(dailyBuildMailUserName,dailyBuildMailPassword)
    smtp.sendmail(msgFrom, msgTo, msg.as_string())
    smtp.quit()

if __name__ == "__main__":
  try:
    mf=open(mailListFile)
    strs=mf.readlines()
    strs=[s.strip() for s in strs if s.find('@') >= 0]
    sendEmail(dailyBuildMailUserName, strs)
    print '... Send email successfully'
  except Exception, e:
    print e
    print '**** Send email failed !!!'
