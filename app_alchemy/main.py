from fastapi import FastAPI
from app.routers.notes import router as notes_router
from app.routers.users import router as users_router
from .routers.crud import router as crud_router
from .dependencies import create_db_and_tables

app = FastAPI()
app.include_router(notes_router)
app.include_router(users_router)
app.include_router(crud_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
