#! /usr/bin/env python
# -*- coding:utf-8 -*-
#usage: python updateEmail.py QRCodePath logString appVersion buildVersion

import sys
import os
import smtplib
import getpass
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.mime.image import MIMEImage

#####################
#   需要配置的参数     #
#####################

# 接受新包邮件的邮箱地址写在mailList.txt里面
mailListFile = 'mailList.txt'
# 本次更新的内容写入log.txt里面
logFile = 'log.txt'
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
QRCodePath = sys.argv[2]
logString = sys.argv[3]
appVersion = sys.argv[4]
buildVersion = sys.argv[5]
debugOrRelease = sys.argv[6]
chineseName = sys.argv[7]
subject = chineseName

def sendEmail(msgFrom, msgTo):
    msg = MIMEMultipart('related') #为了使用attach()
    msg['From'] = msgFrom
    msg['To'] = ','.join(msgTo)
    msg['Subject'] = subject

    # add content
    content = '《' + chineseName + '》' + '版本：' + scheme + '_' + appVersion + '_' + buildVersion + '_' + debugOrRelease + '.app<br />'
    content += '------------------------------------------------------------------------<br />'
    content += '扫码安装：<img alt="" src="cid:image1"/>' + '<br />'
    content += '------------------------------------------------------------------------<br />'

    log=open(logFile)
    strs=log.readlines()
    if len(strs) > 0:
        for s in strs:
            content += s
            content += '<br />'
        content += '------------------------------------------------------------------------<br />'
    log.close()
    log=open(logFile, 'w')
    log.close()

    content += 'svn日志：<br />&nbsp;&nbsp;&nbsp;&nbsp;'
    content += '<br />&nbsp;&nbsp;&nbsp;&nbsp;'.join(logString.split('#'))
    content += '<br /><br />'
    content += 'Author: '
    content += author_dict[getpass.getuser()]
    content += '<br /><br />'

    msgText = MIMEText(content, 'html', 'utf-8')
    msg.attach(msgText)

    # add QRCode
    fp = open(QRCodePath, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

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
