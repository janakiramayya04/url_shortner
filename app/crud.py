import hashlib
import base64
from sqlalchemy.orm import Session
from .models import URLST, Status
from fastapi import HTTPException,status

# crud.py
def status_click(db: Session, url_entry: URLST):
    if not url_entry or not url_entry.id:
        raise HTTPException(status_code=400, detail="Invalid URL entry")

    new_status = Status(url_id=url_entry.id)
    db.add(new_status)
    db.commit()
    db.refresh(new_status)

    return new_status


# def get_click_count(db: Session, keyword: str):
#     url_entry = db.query(URLST).filter(URLST.keyword == keyword).first()
#     if not url_entry:
#         raise HTTPException(status_code=404, detail="URL not found")
#     return len(url_entry.statuses)

def custom_keyword_create(keyword: str, db: Session, url: str):
    if len(keyword) != 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The custom keyword must be exactly 6 characters long."
        )
   
    db_url = URLST(keyword=keyword, url=url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    print(db_url.keyword,db_url.url)
    return db_url


def get_status(keyword: str, db: Session):
    k_p = db.query(URLST).filter(URLST.keyword == keyword).first()
    if not k_p:
        raise HTTPException(status_code=404, detail="Keyword not found")
    
    count = len(k_p.statuses)  
    clicks = [{"timestamp": status.timestamp} for status in k_p.statuses]

    return k_p.keyword, k_p.url, count, clicks


def get_all_links(db: Session):
    urls = db.query(URLST.keyword, URLST.url).all()
    return [{"keyword": k, "url": u} for k, u in urls]


def isexist_to_direct(get_url: str, db: Session):
    url_row = db.query(URLST).filter(URLST.keyword == get_url).first()
    if url_row:
        return url_row
    return None


def delete_link(secret_key: str, db: Session):
    url = db.query(URLST).filter(URLST.keyword== secret_key).first()
    if not url:
        raise HTTPException(
            status_code=404,
            detail="No URL found with the given secret key."
        )

    db.delete(url)
    db.commit()
    return url.keyword,url.url



def isexist(shorturl: str, db: Session) -> bool:
    return db.query(URLST).filter(URLST.keyword == shorturl).first() is not None


def hash_url_short(url: str, db: Session) -> str:
    length = 6
    salt = 0

    while True:
        salted_url = f"{url}{salt}"
        hash_bytes = hashlib.sha256(salted_url.encode()).digest()
        b64 = base64.urlsafe_b64encode(hash_bytes).decode()
        short_key = b64[:length]

        if not isexist(short_key, db):
            return short_key
        salt += 1
