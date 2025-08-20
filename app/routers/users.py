from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Any

from app.dependencies import get_current_active_user, mock_user_db
from ..schemas.users import User, UserInDB

router = APIRouter(prefix="/api", tags=["Account"])



def fake_hash_password(password: str):
    return f"fakehashed{password}"


@router.post("/login")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = mock_user_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def get_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return  current_user
