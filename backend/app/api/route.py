from fastapi import APIRouter
from .v1.route import router as v1_route
from  .sockets import sio_app

router = APIRouter()

router.include_router(v1_route)
router.mount("/socket.io", app=sio_app)

