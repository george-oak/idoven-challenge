from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.database.user_repository import (
    check_username_already_exists,
    create_user_on_db,
    get_user_by_username
)
from src.models.user_model import (
    CreateUserRequest,
    CreateUserResponse
)
from src.database.dependency import db_dependency
from src.database.database_models import DBUser
from src.oauth.oauth import (
    current_user,
    hash_password,
    encode_token
)

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post("/login")
async def login(
    db: db_dependency,
    request: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = get_user_by_username(request.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if not hash_password(request.password) == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong password"
        )
    token = encode_token({
        "username": user.username,
        "is_admin": user.is_admin
    })
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", status_code=201)
async def create_user(
    user_request: CreateUserRequest,
    db: db_dependency,
    user: DBUser = Depends(current_user)
) -> CreateUserResponse:
    if user.is_admin == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if check_username_already_exists(user_request.username, db) is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user with this username already exists"
        )
    user_request.password = hash_password(user_request.password)
    user_created = create_user_on_db(user_request, db)
    return CreateUserResponse(id=user_created.id)
