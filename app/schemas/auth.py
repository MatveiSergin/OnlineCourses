import uuid

from fastapi_users import schemas
from pydantic import BaseModel

from enam import Role


class UserOut(BaseModel):
    name: str
    surname: str


class User(UserOut):
    role: Role = Role.STUDENT


class UserRead(schemas.BaseUser[uuid.UUID], User): ...


class UserCreate(schemas.BaseUserCreate, User): ...


class UserUpdate(schemas.BaseUserUpdate, User): ...
