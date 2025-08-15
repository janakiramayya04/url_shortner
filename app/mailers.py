from email import message
import html
import os
from token import NAME
from dotenv import load_dotenv
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP

from app.schemas import MailBody
load_dotenv()

HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD")
PORT = os.environ.get("MAIL_PORT", 587)
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_STARTTLS = True,
MAIL_SSL_TLS = False,
USE_CREDENTIALS = True,
VALIDATE_CERTS = True

def send_mail(data:dict|None=None):
    msg=MailBody(**data)
    message= MIMEText(msg.body,"html")
    message["From"]=USERNAME
    message["To"]=",".join(msg.to)
    message["Subject"]=msg.subject

    ctx=create_default_context()
    try:
        with SMTP(HOST,PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(
                USERNAME,PASSWORD
            )
            server.send_message(message)
            server.quit()
        return {"status":200,"erros":"none"}
    except Exception as e:
        return {"status":500,"errors":e}