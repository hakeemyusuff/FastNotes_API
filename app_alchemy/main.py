from fastapi import FastAPI
from app_alchemy.routers.notes_router import router as notes_router
from .dependencies import Base, engine

app = FastAPI(title="FastNotes API")

Base.metadata.create_all(engine)

app.include_router(notes_router)



