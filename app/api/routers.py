from fastapi import APIRouter

from api.endpoints.courses import courses_router

common_router = APIRouter(prefix="/api")

for router in (courses_router,):
    common_router.include_router(router)
