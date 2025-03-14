from fastapi import APIRouter
from . import drinks, retrieve, generate

router = APIRouter(
    prefix="/v1",
    tags=["V1"],
)

router.include_router(drinks.router)
router.include_router(retrieve.router)
router.include_router(generate.router)
