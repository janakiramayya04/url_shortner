from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from . import schemas
from . import database
from . import models
from . import crud
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(
    title="URL Shortener", description="A simple API to shorten URLs.", version="1.0.0"
)
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/url")
def url_post(url: schemas.Urlryic, db: Session = Depends(database.get_db)):
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="url is empty"
        )

    short_key = crud.hash_url_short(url.long_url, db)

    short_url = f"http://127.0.0.1:8000/{short_key}"  # Compose full URL

    db_url = models.URLST(keyword=short_key, url=url.long_url)
    db.add(db_url)
    db.commit()

    return {"short_url": short_url}


@app.get("/{get_key}")
def url_key(get_key: str, db: Session = Depends(database.get_db)):
    original_url = crud.isexist_to_direct(get_key, db)
    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Keyword not found"
        )
    crud.status_click(db=db, url_entry=original_url)
    return RedirectResponse(url=original_url.url)


@app.get("/admin/all")
def admin_key(db: Session = Depends(database.get_db)):
    rls = crud.get_all_links(db)
    return rls


@app.delete("/admin/{secrect_key}")
def admin_delete(secrect_key: str, db: Session = Depends(database.get_db)):
    delkey, delurl = crud.delete_link(secrect_key, db)
    return {"keyword": delkey, "url": delurl}


@app.get("/stats/{secret_key}")
def status_checker(secret_key: str, db: Session = Depends(database.get_db)):
    keyword, url, count, clicks = crud.get_status(secret_key, db)
    return {"keyword": keyword, "url": url, "statuses": count, "clicks": clicks}


@app.get("/analytics/{keyword}")
def render_analytics_page(request: Request, keyword: str):
    return templates.TemplateResponse("stats.html", {"request": request})


@app.post("/custom/{keyword}")
def custom_key(
    keyword: str, url_data: schemas.URLBase, db: Session = Depends(database.get_db)
):
    created_url_entry = crud.custom_keyword_create(
        keyword=keyword, db=db, url=str(url_data.long_url)
    )
    print(created_url_entry.url, created_url_entry.keyword)
    return {created_url_entry.keyword, created_url_entry.url}


@app.post("/login/", status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    # Filter search for user
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_verified != True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Account Not Verified"
        )
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post(
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
