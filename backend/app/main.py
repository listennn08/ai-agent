from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console output
        # logging.FileHandler("app.log"),  # Uncomment to log to a file
    ],
)
main_logger = logging.getLogger("sipp")
main_logger.setLevel(logging.DEBUG)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def mount_routers(app: FastAPI):
    from app.controllers.route import router
    from app.controllers.sockets import sio_app

    app.include_router(router)
    app.mount("/socket.io", app=sio_app)


mount_routers(app)
