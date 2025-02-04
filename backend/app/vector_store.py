import os
import faiss
from langchain_community.document_loaders import CSVLoader
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from llm import embeddings


# Initialize FAISS
index = faiss.IndexFlatL2(len(embeddings.embed_query(" ")))
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

# Create a retriever from the vector store
retriever = vector_store.as_retriever()


def initializeVectorStore():
    # check folder `app/storage` exists
    print("Checking Vector Store...")
    if not os.path.exists("./app/storage"):
        os.makedirs("./app/storage")

    # read folder from `app/storage`
    for file in os.listdir("./app/storage"):
        if file.endswith(".csv"):
            # Load Recipes from CSV
            recipes = CSVLoader(f"./app/storage/{file}").load_and_split()
            # Add Recipes to Vector Store
            vector_store.add_documents(recipes)
            print(f"\t - Added {file} to Vector Store")
    print("Vector Store initialized")



initializeVectorStore()