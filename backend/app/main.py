
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from application.services.ingredient_vocab import IngredientVocabulary
from application.services.faiss_manager import FaissDrinkManager


# Load environment variables from .env file
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    ingredient_vocab = IngredientVocabulary()
    faiss_manager = FaissDrinkManager(ingredient_vocab)

    app.state.ingredient_vocab = ingredient_vocab
    app.state.faiss_manager = faiss_manager

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def get_ingredient_vocab():
    return app.state.ingredient_vocab

def get_faiss_manager():
    return app.state.faiss_manager


def mount_routers(app: FastAPI):
    from api.route import router
    app.include_router(router)


mount_routers(app)
