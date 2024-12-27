from fastapi import APIRouter

from api.endpoints.content import content_router
from api.endpoints.courses import courses_router

common_router = APIRouter(prefix="/api")

for router in (courses_router,
               content_router,
               ):
    common_router.include_router(router)

