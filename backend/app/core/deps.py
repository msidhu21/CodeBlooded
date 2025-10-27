from typing import Generator, Annotated
from fastapi import Depends, Header
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .errors import Forbidden
from ..models.entities import Base

engine = create_engine("sqlite:///./cosc310.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

def require_admin(authorization: Annotated[str | None, Header()] = None):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise Forbidden("Missing or invalid token")
    token = authorization.split(" ", 1)[1]
    if token != "admin":
        raise Forbidden("Admin role required")
    return {"role": "admin"}

