import os
import faiss

from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
from langchain_core.vectorstores import VectorStoreRetriever
from socketio.pubsub_manager import json

from config.settings import settings
from ai.llm import embeddings

index: faiss.IndexFlatL2 = None
vector_store: FAISS = None
retriever: VectorStoreRetriever = None

all_ingredients = set()
ingredient_to_index = []

def _processCSV(file):
    recipes = CSVLoader(f"{settings.STORAGE_FILE_PATH}{file}").load_and_split()
    vector_store.add_documents(recipes)


def _processJSON(file):
    global all_ingredients, ingredient_to_index, index, vector_store
    recipes = json.load(open(f"{settings.STORAGE_FILE_PATH}{file}"))

    # create a ingredient dictionary
    for recipe in recipes:
        for ingredient in recipe.get("ingredients", []):
            all_ingredients.add(ingredient["name"])

    all_ingredients = sorted(list(all_ingredients))
    ingredient_to_index = {ingredient: index for index, ingredient in enumerate(all_ingredients)}

    # d = len(ingredient_to_index)
    # index = faiss.IndexFlatL2(d)
    vectors = []
    # convert drink to ingredient vector
    # for recipe in recipes:
    #     vector = np.zeros(d, dtype=np.float32)
    #     for ingredient in recipe.get("ingredients", []):
    #         if ingredient["name"] in ingredient_to_index:
    #             # use volume ml as weight for ingredient vector
    #             vector[ingredient_to_index[ingredient["name"]]] = ingredient["ratio"]
        
    #     vectors.append(vector)
    

    vector_store.add_documents(vectors)



def _createVectorStore():
    global index, vector_store, retriever
    print("Vector Store not found, initializing...")

    index = faiss.IndexFlatL2(len(embeddings.embed_query("")))
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    # read folder from `app/storage`
    for file in os.listdir("./app/storage/files"):
        if file.startswith("_"):
            continue

        if file.endswith(".csv"):
            _processCSV(file)
        elif file.endswith(".json"):
            _processJSON(file)
        else:
            continue
        
        print(f"\t - Added {file} to Vector Store")
    
    vector_store.save_local("./app/storage/vector_store")
    print("Vector Store initialized")
    retriever =vector_store.as_retriever()


def initializeVectorStore():
    global index, vector_store, retriever
    # check folder `app/storage` exists
    print("Checking Vector Store...")
    if not os.path.exists("./app/storage"):
        os.makedirs("./app/storage")

    if not os.path.exists("./app/storage/vector_store"):
        os.makedirs("./app/storage/vector_store")

    if (os.path.exists("./app/storage/vector_store/index.faiss")):
        vector_store = FAISS.load_local("./app/storage/vector_store", embeddings=embeddings, allow_dangerous_deserialization=True)
        index = vector_store.index
        print("Vector Store loaded")
    else:
        _createVectorStore()
        


initializeVectorStore()