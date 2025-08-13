from time import timezone
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    TIMESTAMP,
    text,
    Boolean,
)
from datetime import datetime
from .database import Base
from sqlalchemy.orm import relationship

# URLST model
class URLST(Base):
    __tablename__ = "url_shortner"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(15), unique=True, index=True)
    url = Column(String(2048), nullable=False)
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    owner = relationship("Users")
    statuses = relationship(
        "Status", back_populates="url_entry", cascade="all, delete-orphan"
    )


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String(100),nullable=False)
    email = Column(String(20), nullable=False)
    password = Column(String(100), nullable=False)
    status = Column(Boolean, server_default="1", nullable=False)
    isverified = Column(Boolean, server_default="0", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# Status model
class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    url_id = Column(Integer, ForeignKey("url_shortner.id"), nullable=False)
    url_entry = relationship("URLST", back_populates="statuses")
