
# coding: utf-8

# In[ ]:


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
 
def sendemail(login, password,
              to_addr_list,
              subject, 
              message,
              smtpserver='smtp.gmail.com:587'):


    msg = MIMEMultipart()

    msg['From'] = login
    msg['To'] = to_addr_list
    msg['Subject'] = subject

    body = "TEXT YOU WANT TO SEND"

    msg.attach(MIMEText(body, 'plain'))

    filename = "bittrex_USDT-OMG_hour.png"
    attachment = open("bittrex_USDT-OMG_hour.png", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(login,password)
    text = msg.as_string()
    problems = server.sendmail(login, to_addr_list, text)
    server.quit()
    return problems


# In[ ]:


sendemail(login        = 'ucemso2@gmail.com', 
          password     = '',
          to_addr_list = ['ucemso1@gmail.com'],
          subject      = 'Howdy', 
          message      = 'Howdy from a python function') 
          


# In[ ]:


login        = 'ucemso2@gmail.com'
password     = ''
to_addr_list = ['ucemso1@gmail.com']
subject      = 'Howdy'
message      = 'Howdy from a python function'

msg = MIMEMultipart()

msg['From'] = login
msg['To'] = to_addr_list
msg['Subject'] = subject

body = "TEXT YOU WANT TO SEND"

msg.attach(MIMEText(body, 'plain'))

filename = "bittrex_USDT-OMG_hour.png"
attachment = open("bittrex_USDT-OMG_hour.png", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(login,password)
text = msg.as_string()
problems = server.sendmail(login, to_addr_list, text)
server.quit()
return problems


# In[ ]:


import plot_candle_and_volume

