from fastapi import APIRouter, status, Request, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])

from .. import schemas
from .. import database
from .. import models
from .. import oauth
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    if user.isverified != True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Account Not Verified"
        )
    access_token = oauth.create_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify")
def verification(email: schemas.UserLogin, db: Session = Depends(database.get_db)):
    verify_link = oauth.create_email_token(email, db)
    return verify_link


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(database.get_db)):
    oauth.verify_email(token, db)
    return {"message": "verified email "}
