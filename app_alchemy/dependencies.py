from typing import Annotated
from fastapi import Depends, status, HTTPException, Query
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base


DATABASE_FILENAME = "new_note.db"
DATABASE_URL = f"sqlite:///app_alchemy/{DATABASE_FILENAME}"
connection_arg = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connection_arg)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db()

sessionDep = Annotated[Session, Depends(get_db)]
