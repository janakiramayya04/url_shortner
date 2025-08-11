from jose import JWTError, jwt,ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from fastapi.security.oauth2 import OAuth2PasswordBearer
from .database import get_db
from .schemas import TokenData
from app import models

from app import schemas

from app import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
load_dotenv(dotenv_path=".env")
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_email_token(user: schemas.UserLogin, db: Session):
    user_in_db = db.query(models.Users).filter(models.Users.email== user.email).first()
    print(user_in_db, user.email)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")
    token = jwt.encode(
        {
            "sub": user.email,
            "type": "email_verification",
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=5),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    verify_link = f"http://localhost:8000/verify-email?token={token}"
    # Send email with verify_link here
    return verify_link


def verify_email(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = db.query(models.Users).filter(models.Users.email == email).first()
        print(user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.isverified = True
        db.commit()
        return {"message": "Email verified successfully"}
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        id_str: str = str(id)
        token_data = TokenData(id=id_str)
    except JWTError:
        raise credentials_exception

    return token_data


def get_curr_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not valid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    try:
        user_id_int = int(token.id)
    except ValueError:
        raise credentials_exception
    user = db.query(models.User).filter(models.Users.id == user_id_int).first()
    return user
