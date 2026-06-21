import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time

data = json.loads('weibo_hot_searches.json')

# 邮箱配置
smtp_server = 'smtp.example.com'
smtp_port = 587
sender_email = 'your_email@example.com'
sender_password = 'your_password'
receiver_email = 'receiver_email@example.com'

def send_email(content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header(sender_email)
    msg['To'] = Header(receiver_email)
    msg['Subject'] = Header('微博热搜数据')

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

while True:
    email_content = json.dumps(data, ensure_ascii=False, indent=2)
    send_email(email_content)
    time.sleep(20)
