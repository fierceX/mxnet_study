
# coding: utf-8

import poplib
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from envelopes import Envelope
import email


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def Get_info(msg):
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            return Get_info(part)
    if not msg.is_multipart():
        content_type = msg.get_content_type()
        if content_type=='text/plain':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            return content

def SentEmail(message,subject):
    envelope = Envelope(
    from_addr=(u'trainmonitor@126.com', u'Train'),
    to_addr=(u'fiercewind@outlook.com', u'FierceX'),
    subject=subject,
    text_body=message
    )
    
    envelope.add_attachment('1.png')
    
    envelope.send('smtp.126.com', login='trainmonitor@126.com',
              password='mxnet123', tls=True)
    
def ReEmail():
    host = "pop.126.com"
    user = "trainmonitor@126.com"
    password = "mxnet123"
    try:
        pp = poplib.POP3(host)
        pp.user(user)
        pp.pass_(password)
        resp, mails, octets = pp.list()
        index = len(mails)
        if index > 0:
            resp, lines, octets = pp.retr(index)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            pp.dele(index)
            pp.quit()
            msg = Parser().parsestr(msg_content)
            message = Get_info(msg)
            subject = msg.get('Subject')
            date = msg.get('Date')
            return message,subject,date
    except ConnectionResetError as e:
        print('ConnectionResetError')
    return None,None,None

