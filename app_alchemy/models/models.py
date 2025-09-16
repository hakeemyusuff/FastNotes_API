from sqlalchemy import Column, Integer, String, DateTime, func
from ..dependencies import Base




class Note(Base):
    __tablename__ = "Notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    body = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    edited_at = Column(DateTime(timezone=True), onupdate=func.now())
