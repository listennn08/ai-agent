import sys
import uuid
import logging

sys.path.append("/Users/matt/dev/rag-agent/backend/app")

import os
import faiss
import numpy as np

from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
from langchain_core.vectorstores import VectorStoreRetriever
from socketio.pubsub_manager import json

# from app.repositories.drink_repository import DrinkRepository, get_db
from application.ai.llm import embeddings

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
    filemode="a",
    filename="vector_store.log",
)

index: faiss.IndexFlatL2 = None
vector_store: FAISS = None
retriever: VectorStoreRetriever = None

# drink_repository = DrinkRepository(get_db())
all_ingredients = set()
ingredient_to_index = []

def _processCSV(file):
    global index, vector_store
    index = faiss.IndexFlatL2(len(embeddings.embed_query("")))
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    recipes = CSVLoader(f"./app/storage/{file}").load_and_split()
    vector_store.add_documents(recipes)
    vector_store.save_local("./app/storage/vector_store")


def _processJSON(file):
    global all_ingredients, ingredient_to_index, index, vector_store
    recipes = json.load(open(f"./app/storage/{file}"))

    # create a ingredient dictionary
    for recipe in recipes:
        for ingredient in recipe.get("ingredients", []):
            all_ingredients.add(ingredient["name"])

    all_ingredients = sorted(list(all_ingredients))
    logging.debug(f"all_ingredients: {all_ingredients}")
    ingredient_to_index = {ingredient: index for index, ingredient in enumerate(all_ingredients)}

    # print(all_ingredients)
    d = len(ingredient_to_index)
    index = faiss.IndexFlatL2(d)
    vectors = []
    # convert drink to ingredient vector
    for recipe in recipes:
        vector = np.zeros(d, dtype=np.float32)
        for ingredient in recipe.get("ingredients", []):
            if ingredient["name"] in ingredient_to_index:
                # use volume ml as weight for ingredient vector
                vector[ingredient_to_index[ingredient["name"]]] = ingredient["ratio"]
        
        logging.debug(f"vector: {vector.tolist()}")
        vectors.append(vector)
    

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    ids = [str(uuid.uuid4()) for _ in vectors]

    vector_store.add_documents(vectors, ids=ids)

    vector_store.save_local("./app/storage/vector_store")



def _createVectorStore():
    global index, vector_store
    logging.info("Vector Store not found, initializing...")

    # read folder from `app/storage`
    for file in os.listdir("./app/storage"):
        if file.endswith(".csv"):
            pass
            # _processCSV(file)
        elif file.endswith(".json"):
            _processJSON(file)
        else:
            continue
        
        logging.info(f"\t - Added {file} to Vector Store")
    
    logging.info("Vector Store initialized")


def initializeVectorStore():
    global index, vector_store, retriever
    # check folder `app/storage` exists
    logging.info("Checking Vector Store...")
    if not os.path.exists("./app/storage"):
        os.makedirs("./app/storage")

    if not os.path.exists("./app/storage/vector_store"):
        os.makedirs("./app/storage/vector_store")

    if (os.path.exists("./app/storage/vector_store/index.faiss")):
        vector_store = FAISS.load_local("./app/storage/vector_store", embeddings=embeddings, allow_dangerous_deserialization=True)
        index = vector_store.index
        logging.info("Vector Store loaded")
    else:
        _createVectorStore()
        
    
    # retriever = vector_store.as_retriever()


initializeVectorStore()


if __name__ == "__main__":
    # results = vector_store.similarity_search_with_score("Strawberry", k=5)
    # convert to json format
    # json_results = [{"doc": result[0].page_content, "score": result[1]} for result in results]
    
    # print(json_results)
    # initializeVectorStore()
    pass