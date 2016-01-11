# -*- coding:utf-8 -*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.text import MIMEText
import smtplib


def sendPasswordByEmail(useraddress, password, username):
    mailbody = readMailBody('FindPasswordMailBody.txt') + password
    sendMail(useraddress, username, '找回拐杖的密码', mailbody)

def readMailBody(textFile):
    with open('./common/config/' + textFile) as f:
        body = f.read()
    return body

def sendAuthLinkByEmail(useraddress, username, authlink):
    mailbody = readMailBody('AuthLinkMailBody.txt') + authlink
    sendMail(useraddress, username, '认证邮箱链接', mailbody)

def sendMail(mailaddress, username, mailsubject, mailbody):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((\
                Header(name, 'utf-8').encode(), \
                addr.encode('utf-8') if isinstance(addr, unicode) else addr ))

    with open('./common/mail_account.config', 'r') as f:
        config = eval(f.read())
    msg = MIMEText(mailbody, 'plain', 'utf-8')
    msg['From'] = _format_addr('hult <%s>' % config['account'])
    msg['To'] = _format_addr('%s <%s>' % (username, mailaddress))
    msg['Subject'] = Header(mailsubject, 'utf-8').encode()

    server = smtplib.SMTP(config['smtpserver'], 587)
    server.set_debuglevel(False)
    try:
        server.starttls()
        server.login(config['account'], config['password'])
        server.sendmail(config['account'], mailaddress, msg.as_string())
    except Exception as e:
        with open('./mail.log' ,'a') as f:
            f.write(str(e))
    finally:
	server.quit()



if __name__ == '__main__':
    sendAuthLinkByEmail('kindth@qq.com', 'hult', 'http://www.huahailife.com')
    #sendPasswordByEmail('htang@pku.edu.cn', '1234', 'hult')
    #sendMail('kindth@qq.com', 'hult', '验证链接测试', readMailBody('AuthLinkMailBody.txt'))
