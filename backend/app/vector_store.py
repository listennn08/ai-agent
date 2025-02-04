import os
import faiss
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS

from llm import embeddings


# d = len(embeddings.embed_query(" "))
d = 128
print('Dimensionality: ', d)
# Initialize FAISS
index = faiss.IndexFlatL2(d)
vector_store: FAISS = None
# FAISS(
#     embedding_function=embeddings,
#     index=index,
#     docstore=InMemoryDocstore(),
#     index_to_docstore_id={},
# )

# Create a retriever from the vector store
# retriever = vector_store.as_retriever()


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
            for recipe in recipes:
                print(recipe)
                print('-'*50)

            # Add Recipes to Vector Store
            global vector_store
            vector_store = FAISS.from_documents(recipes, embedding=embeddings)
            print(f"\t - Added {file} to Vector Store")
    print("Vector Store initialized")


initializeVectorStore()

print(vector_store.similarity_search_with_score("rum", k=3))