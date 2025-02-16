
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from services.drink_retrieve_service import DrinkRetrieveService


# Load environment variables from .env file
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    drink_retrieve_service = DrinkRetrieveService()
    app.state.drink_retrieve_service = drink_retrieve_service

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def mount_routers(app: FastAPI):
    from api.route import router
    app.include_router(router)


mount_routers(app)
