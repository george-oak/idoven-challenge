from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.database.dependency import db_dependency
from src.database.database_models import DBUser
from passlib.context import CryptContext
from src.database.user_repository import get_user_by_username
from jose import jwt


oauth2 = OAuth2PasswordBearer(tokenUrl="/user/login")
crypt = CryptContext(schemes=["bcrypt"])
# TODO: Create env variable
SECRET = "secret-value"
ALGORITHM = "HS256"


async def current_user(
    db: db_dependency,
    token: str = Depends(oauth2)
) -> DBUser:
    token_decoded = decode_token(token)
    user = get_user_by_username(token_decoded.get("username"), db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"})
    return user


def encode_token(payload: dict) -> str:
    return jwt.encode(payload, SECRET, ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET, ALGORITHM)


def hash_password(password: str) -> str:
    return jwt.encode({"password": password}, SECRET, ALGORITHM)
