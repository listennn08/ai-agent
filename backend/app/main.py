from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def mount_routers(app: FastAPI):
    from api.route import router
    from api.sockets import sio_app

    app.include_router(router)
    app.mount("/socket.io", app=sio_app)


mount_routers(app)
