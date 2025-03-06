import sys
# import uuidx
import logging
# import json
import os

sys.path.append("/Users/matt/dev/rag-agent/backend/app")

# import numpy as np

from langchain_community.document_loaders import CSVLoader, JSONLoader

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
    filemode="a",
    filename="vector_store.log",
)


def _processCSV(file):
    result = CSVLoader(f"./app/storage/{file}").load_and_split()
    return result


def _processJSON(file):
    result = JSONLoader(f"./app/storage/files/${file}", jq_schema=".[]")
    return result



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
        # vector_store = FAISS.load_local("./app/storage/vector_store", embeddings=embeddings, allow_dangerous_deserialization=True)
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