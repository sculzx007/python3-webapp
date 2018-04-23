#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib

#用于格式化邮件地址
def _format_addr(s):
    name, addr = parseaddr(addr)
    return formataddr(Header(name, 'utf-8').encode(), addr)

#Email地址和密码
from_addr = input('From:')
password = input('Password:')

#收件人地址
to_addr = input('To:')

#输入SMTP服务器地址
smtp_server = input('SMTP server:')

#发送的邮件内容
msg = MIMEText('Hello, send by Python...', 'plain', 'utf-8')

#邮件中显示的发件人信息
msg['From'] = _format_addr('发件人 <%s>' % from_addr)

#邮件中显示的收件人信息
msg['To'] = _format_addr('收件人 <%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

#设置SMTP服务器
server = smtplib(smtp_server, 25)
server.set_debuglevel(1)
server.login(_format_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
