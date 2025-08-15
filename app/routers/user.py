from fastapi import APIRouter , BackgroundTasks, Depends, Request
from sqlalchemy.orm import Session

from app import database

from .. import schemas
from .. import config
from .. import oauth
from .. import mailer
router = APIRouter(prefix="/jr", tags=["Send Email"])

@router.post("/forgot")
async def forgot_password(email:schemas.forgotPassword,tasks: BackgroundTasks, request: Request,db:Session=Depends(database.get_db)):
    user_mail=email.email
    email_string = user_mail[0] if isinstance(user_mail, list) else user_mail
    print(email_string)
    token_data = {"sub": email_string} 
    token = oauth.create_verification_token(token_data)
    print(token)
    forgot_url =f"{request.base_url}auth/reset?token={token}"
    html_content = f"""
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
            <h2>Welcome! Please reset Your Password</h2>
            <p>Thanks for login. Please click the button below to verify your email address.</p>
            <a href="{forgot_url}"
               style="background-color: #007BFF; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;">
               Verify My Email
            </a>
            <p style="margin-top: 30px; font-size: 0.9em; color: #777;">
                If the button doesn't work, you can copy and paste this link into your browser:<br>
                <a href="{forgot_url}">{forgot_url}</a>
            </p>
        </div>
    </body>
    </html>
    """
    tasks.add_task(
        mailer.send_mail,
        recipient_email=email.email,
        subject="Reset Your Password",
        html_body=html_content
    )
    return {"message": "If an account with that email exists, a reset link has been sent."}


@router.post("/send-email")
async def send_email(req: schemas.EmailSchema,tasks: BackgroundTasks, request: Request):
    
    # 1. Generate a verification token containing the user's email
    user_email = req.email # Assuming MailBody schema has an 'email' field
    email_string = user_email[0] if isinstance(user_email, list) else user_email
    token_data = {"sub": email_string} 
    token = oauth.create_verification_token(token_data)
    
    # 2. Construct the full verification URL
    # request.base_url gives you "http://127.0.0.1:8000/" or "https://yourapp.com/"
    verification_url = f"{request.base_url}auth/verify-email?token={token}"
    
    # 3. Create a nice HTML body for the email
    html_content = f"""
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
            <h2>Welcome! Please Verify Your Email</h2>
            <p>Thanks for signing up. Please click the button below to verify your email address.</p>
            <a href="{verification_url}"
               style="background-color: #007BFF; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;">
               Verify My Email
            </a>
            <p style="margin-top: 30px; font-size: 0.9em; color: #777;">
                If the button doesn't work, you can copy and paste this link into your browser:<br>
                <a href="{verification_url}">{verification_url}</a>
            </p>
        </div>
    </body>
    </html>
    """
    
    # 4. Schedule the email to be sent in the background
    tasks.add_task(
        mailer.send_mail,
        recipient_email=req.email,
        subject="Please Verify Your Email Address",
        html_body=html_content
    )
    
    return {"status": 200, "message": "Verification email has been scheduled."}
# async def send_email(email: schemas.EmailSchema):
#     """
#     Sends an email to the recipient specified in the request body.
#     """
#     html_content = """
#     <html>
#         <body>
#             <h1>Hello from FastAPI!</h1>
#             <p>This is a test email sent from a FastAPI application using fastapi-mail.</p>
#             <p>Current Time in Vijayawada: 13 August 2025, 11:42 AM IST</p>
#         </body>
#     </html>
#     """

#     message = MessageSchema(
#         subject="FastAPI Mail Test",
#         recipients=email.email,  # Get recipient list from Pydantic model
#         body=html_content,
#         subtype=MessageType.html
#     )

#     fm = FastMail(config.conf)
#     try:
#         await fm.send_message(message)
#         return {"status": "success", "message": "Email has been sent"}
#     except Exception as e:
#         # In a real app, you'd want more robust error handling and logging
#         return {"status": "error", "message": f"Failed to send email: {e}"}


