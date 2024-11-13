from sqlalchemy.orm import Session
from src.database.database_models import DBUser
from src.models.user_model import CreateUserRequest


# TODO: Create Class
def check_username_already_exists(username: str, db: Session) -> bool:
    user = get_user_by_username(username, db)
    if user is None:
        return False
    return True


def get_user_by_username(username: str, db: Session) -> DBUser | None:
    return db.query(DBUser).filter(DBUser.username == username).first()


def create_user_on_db(
    user_request: CreateUserRequest,
    db: Session
) -> DBUser:
    user = DBUser(
        username=user_request.username,
        password=user_request.password,
        is_admin=user_request.is_admin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
