import json
from typing import Annotated
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends
from langchain_core.documents import Document
from infrastructure.vector_store.vector_store import VectorStore
from depends import get_vector_store


router = APIRouter(
    prefix="/drinks",
    tags=["Drinks"],
)

folder_path = Path("./app/storage/vector_store")


@router.post("/")
def add_drinks(
    file: UploadFile = Annotated[bytes, File()],
    vc: VectorStore = Depends(get_vector_store),
):
    drinks = json.loads(file.file.read())
    docs = []
    for drink in drinks:
        docs.append(
            Document(page_content=json.dumps(drink), metadata={"source": "drinks"})
        )

    vc.vector_store.add_documents(docs)
    vc.vector_store.save_local(folder_path)

    return {"message": "Drinks added", "drinks": docs}
