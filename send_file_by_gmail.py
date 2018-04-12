
# coding: utf-8

# In[1]:


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
 
fromaddr = "ucemso2@gmail.com"
password = ""
toaddr = "ucemso1@gmail.com"
subject = "SUBJECT OF THE EMAIL"
body = "TEXT YOU WANT TO SEND"
filename_list = ["bittrex_USDT-OMG_hour.png", "output.png", "Bittrex_API_document.docx"]

msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = subject
 
 
msg.attach(MIMEText(body, 'plain'))

for filename in filename_list:
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, password)
text = msg.as_string()
problem = server.sendmail(fromaddr, toaddr, text)
server.quit()

