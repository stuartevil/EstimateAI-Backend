"""API v1 routers."""

from fastapi import APIRouter

from app.api.v1.ai_router import router as ai_router
from app.api.v1.annotation_router import router as annotation_router
from app.api.v1.auth_router import router as auth_router
from app.api.v1.drawing_router import router as drawing_router
from app.api.v1.measurement_router import router as measurement_router
from app.api.v1.project_router import router as project_router
from app.api.v1.takeoff_router import router as takeoff_router
from app.api.v1.user_router import router as user_router

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router)
api_v1_router.include_router(user_router)
api_v1_router.include_router(project_router)
api_v1_router.include_router(drawing_router)
api_v1_router.include_router(annotation_router)
api_v1_router.include_router(measurement_router)
api_v1_router.include_router(takeoff_router)
api_v1_router.include_router(ai_router)
