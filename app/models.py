from time import timezone
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime,TIMESTAMP,text
from datetime import datetime
from .database import Base
from sqlalchemy.orm import relationship

# URLST model
class URLST(Base):
    __tablename__ = "url_shortner"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(15), unique=True, index=True)
    url = Column(String(2048), nullable=False)

    statuses = relationship("Status", back_populates="url_entry", cascade="all, delete-orphan")


# Status model
class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    url_id = Column(Integer, ForeignKey("url_shortner.id"), nullable=False)
    url_entry = relationship("URLST", back_populates="statuses")
