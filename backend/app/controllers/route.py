from fastapi import APIRouter
from app.controllers.v1.route import router as v1_route

router = APIRouter()

router.include_router(v1_route)
