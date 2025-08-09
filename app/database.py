from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
