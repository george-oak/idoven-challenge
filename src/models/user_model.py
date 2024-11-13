from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str
    password: str
    is_admin: int = Field(ge=0, le=1)

    model_config = {
        'json_schema_extra': {
            'example': {
                'username': 'email@sample.com',
                'password': '123_Answer_again',
                'is_admin': 0
            }
        }
    }


class CreateUserResponse(BaseModel):
    id: int

    model_config = {
        'json_schema_extra': {
            'example': {
                'id': '1'
            }
        }
    }


class LoginResquest(BaseModel):
    username: str
    password: str

    model_config = {
        'json_schema_extra': {
            'example': {
                'username': 'email@sample.com',
                'password': '123_Answer_again'
            }
        }
    }
