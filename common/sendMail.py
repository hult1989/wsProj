from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.text import MIMEText
import smtplib


def sendPasswordByEmail(useraddress, password):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((\
                Header(name, 'utf-8').encode(), \
                addr.encode('utf-8') if isinstance(addr, unicode) else addr ))

    with open('./common/mail_account.config', 'r') as f:
        config = eval(f.read())
    
    msg = MIMEText('hello, your password is:\t%s' % password, 'plain', 'utf-8')
    msg['From'] = _format_addr('hult <%s>' % config['account'])
    msg['To'] = _format_addr('SomeOne <%s>' %useraddress)
    msg['Subject'] = Header('This is your password', 'utf-8').encode()

    server = smtplib.SMTP(config['smtpserver'], 587)
    server.starttls()
    server.set_debuglevel(1)
    server.login(config['account'], config['password'])
    server.sendmail(config['account'], useraddress, msg.as_string())
    server.quit()




if __name__ == '__main__':
    sendPasswordByEmail('htang@pku.edu.cn', '1234')
