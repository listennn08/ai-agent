import os
import faiss

from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from socketio.pubsub_manager import json

from llm import embeddings


index: faiss.IndexFlatL2 = None
vector_store: FAISS = None
retriever: VectorStoreRetriever = None

def _processCSV(file):
    recipes = CSVLoader(f"./app/storage/{file}").load_and_split()
    # vector_store.add_documents(recipes)


def _processJSON(file):
    recipes = json.load(open(f"./app/storage/{file}"))

    for recipe in recipes:
        ingredients = recipe.get("ingredient", [])
        print(ingredients)


    # vector_store.add_documents(recipes)


def _createVectorStore():
    global index, vector_store
    print("Vector Store not found, initializing...")
    # Initialize FAISS
    # index = faiss.IndexFlatL2(len(embeddings.embed_query(" ")))
    # vector_store = FAISS(
    #     embedding_function=embeddings,
    #     index=index,
    #     docstore=InMemoryDocstore(),
    #     index_to_docstore_id={},
    # )
    # read folder from `app/storage`
    for file in os.listdir("./app/storage"):
        if file.endswith(".csv"):
            _processCSV(file)
        elif file.endswith(".json"):
            _processJSON(file)
        else:
            continue
        
        print(f"\t - Added {file} to Vector Store")
    
    # vector_store.save_local("./app/storage/vector_store")
    print("Vector Store initialized")


def initializeVectorStore():
    global vector_store, retriever
    # check folder `app/storage` exists
    print("Checking Vector Store...")
    if not os.path.exists("./app/storage"):
        os.makedirs("./app/storage")

    if not os.path.exists("./app/storage/vector_store"):
        os.makedirs("./app/storage/vector_store")

    if (os.path.exists("./app/storage/vector_store/index.faiss")):
        vector_store = FAISS.load_local("./app/storage/vector_store", embeddings=embeddings)
        print("Vector Store loaded")
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