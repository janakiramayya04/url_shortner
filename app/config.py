from fastapi_mail import ConnectionConfig
import os
from dotenv import load_dotenv
load_dotenv()

# Define your configuration once in this file
conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"), # Use an App Password for Gmail
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)