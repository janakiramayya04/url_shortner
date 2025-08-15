from fastapi_mail import FastMail, MessageSchema, MessageType
from typing import List
from .config import conf # Your ConnectionConfig

async def send_mail(recipient_email: List[str], subject: str, html_body: str):
    """
    Sends an email with the given HTML body.
    """
    message = MessageSchema(
        subject=subject,
        recipients=recipient_email,
        body=html_body,
        subtype=MessageType.html
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)