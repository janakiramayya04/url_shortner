from tempfile import template
from fastapi import APIRouter, BackgroundTasks, status, Request, Depends, HTTPException

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates
router = APIRouter(prefix="/auth", tags=["Authentication"])
templates = Jinja2Templates(directory="app/templates")
from .. import schemas
from .. import database
from .. import models
from .. import oauth
from .. import mailer
from .. import crud
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# @router.get("/me")
# def get_profile(current_user: models.Users = Depends(oauth.get_curr_user)):
#     return {"username": current_user.username, "email": current_user.email}


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.RegistrationUserRepsonse,
)
def register(
    request: Request,
    user_credentials: schemas.UserCreate,
    db: Session = Depends(database.get_db),
):
    email_check = (
        db.query(models.Users)
        .filter(models.Users.email == user_credentials.email)
        .first()
    )
    if email_check != None:
        raise HTTPException(
            detail="Email is already registered", status_code=status.HTTP_409_CONFLICT
        )
    hashed_password = pwd_context.hash(user_credentials.password)
    user_credentials.password = hashed_password
    new_user = models.Users(
        username=user_credentials.username,
        email=user_credentials.email,
        password=user_credentials.password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registration successful", "data": new_user}


@router.post("/login", response_model=schemas.Token)
def login(
    request: Request,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.Users)
        .filter(models.Users.username == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not pwd_context.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.isverified != True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Account Not Verified"
        )
    access_token = oauth.create_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/verify")
# def verification(email: schemas.UserLogin, db: Session = Depends(database.get_db)):
#     verify_link = oauth.create_email_token(email, db)
#     return verify_link


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(database.get_db)):
    oauth.verify_email(token, db)
    return {"message":"verification successfull"}


@router.post("/send-verfiymail")
def verfiy_mail(req:schemas.MailBody,tasks:BackgroundTasks):
    data=req.model_dump()
    tasks.add_task(mailer.send_mail,data)
    return{"status":200, "message":"email is scheduled "}

@router.get("/reset")
def verify_reset_token(token: str,request:Request, db: Session = Depends(database.get_db)):
    print(token)
    email = oauth.verify_email_forgot(token, db)
    return templates.TemplateResponse( "forgotpass.html",
        {
            "request": request,
            "email": email,      
            "access_token": token      
        }
)
@router.post("/reset")
def reset_password(payload: schemas.resetPassword, db: Session = Depends(database.get_db)):
    try:
        # Get the email by verifying the token from the payload
        email = oauth.verify_email_forgot(payload.token, db)
    except HTTPException as e:
        raise e # Re-raise the exception if the token is invalid

    # Check if passwords from the payload match
    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match."
        )
        
    # Proceed with resetting the password
    user = crud.reset_password(
        db=db, 
        email=email, 
        new_password=payload.password # Use the validated password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return {"message": "Password has been reset successfully."}
