import logging
import faiss
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
from langchain_core.embeddings import Embeddings

from app.infrastructure.vector_store.base import IVectorStore

main_logger = logging.getLogger("sipp")


class FaissVectorStore(IVectorStore):
    index: faiss.IndexFlatL2 = None
    vector_store: FAISS = None

    def __init__(self, embedding: Embeddings):
        self.embedding = embedding
        self.initialize()

    def batch_insert(self, documents):
        self.vector_store.add_documents(documents)

    def read_index():
        return faiss.read_index

    def initialize(self):
        # check folder `app/storage` exists
        main_logger.info("Checking Vector Store...")
        folder_path = Path("./app/storage/vector_store")
        index_path = Path("./app/storage/vector_store/index.faiss")

        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)

        if index_path.exists():
            self.vector_store = FAISS.load_local(
                "./app/storage/vector_store",
                embeddings=self.embedding,
                allow_dangerous_deserialization=True,
            )
            self.index = self.vector_store.index
            main_logger.info("Vector Store loaded")
        else:
            self.index = faiss.IndexFlatL2(len(self.embedding.embed_query("")))
            self.vector_store = FAISS(
                embedding_function=self.embedding,
                index=self.index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )
