import faiss
from langchain_community.document_loaders import CSVLoader
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from llm import embeddings


# Load Recipes from CSV
recipes = CSVLoader("./app/storage/recipes.csv").load_and_split()

# Initialize FAISS
index = faiss.IndexFlatL2(len(embeddings.embed_query(" ")))
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

# Add Recipes to Vector Store
vector_store.add_documents(recipes)

# Create a retriever from the vector store
retriever = vector_store.as_retriever()