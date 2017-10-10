
# coding: utf-8

# In[132]:


import os
import poplib
import smtplib
import re
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import email


# In[133]:


host = "pop.126.com"
user = "trainmonitor@126.com"
password = "mxnet123"


# In[134]:


pp = poplib.POP3(host)
pp.user(user)
pp.pass_(password)


# In[135]:


resp, mails, octets = pp.list()
index = len(mails)
resp, lines, octets = pp.retr(index)

msg_content = b'\r\n'.join(lines).decode('utf-8')
pp.quit()


# In[138]:


msg = Parser().parsestr(msg_content)


# In[139]:


msg.get('Subject')


# In[84]:


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


# In[160]:


def Get_info(msg):
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            return print_info(part)
    if not msg.is_multipart():
        content_type = msg.get_content_type()
        if content_type=='text/plain':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            return content


# In[161]:


xx = Get_info(msg)
sl = xx.split('\r\n')
params = {}
for s in sl:
    sk = s.split(' ')
    if len(sk) > 1:
        params[sk[0]] = sk[1]
params


# In[181]:


from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# In[187]:


from_addr = 'trainmonitor@126.com'
to_addr = 'fiercewind@outlook.com'
msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
msg['From'] = _format_addr('Python爱好者<%s>' % from_addr)
msg['To'] = _format_addr('fiercewind<%s>' % to_addr)
msg['Subject'] = Header('test', 'utf-8').encode()


# In[188]:


server = smtplib.SMTP_SSL('smtp.126.com') # SMTP协议默认端口是25
server.login(from_addr, 'mxnet123')
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()

