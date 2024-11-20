from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from api.routers import common_router
from user import fastapi_users

from database.utils import create_tables
from schemas.auth import UserRead, UserCreate, UserUpdate
from user import auth_backend


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(title="Online Courses", lifespan=lifespan)

app.include_router(common_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
