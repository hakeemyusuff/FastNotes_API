from fastapi import FastAPI
from app.routers.notes import router as notes_router
from app.routers.users import router as users_router

app = FastAPI()
app.include_router(notes_router)
app.include_router(users_router)

