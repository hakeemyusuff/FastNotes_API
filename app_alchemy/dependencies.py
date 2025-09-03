from fastapi import Depends, status, HTTPException, Query
from sqlmodel import Session, create_engine, SQLModel
from fastapi.security import OAuth2PasswordBearer
from app.schemas.users import UserInDB, User
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

db_filename = "note.db"
db_url = f"sqlite:///{db_filename}"

connect_args = {"check_same_thread": False}
engine = create_engine(db_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

mock_user_db = {
    "testuser": {
        "username": "testuser",
        "email": "test@qa.team",
        "full_name": "test user",
        "disabled": False,
        "hashed_password": "fakehashedpass",
    }
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(mock_user_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    print(token)
    user = fake_decode_token(token)
    print(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user."
        )
    return current_user
