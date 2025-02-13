import os
from uuid import uuid4
from fastapi import APIRouter
from fastapi import UploadFile
from langchain_community.document_loaders import CSVLoader, JSONLoader

from app.vector_store import vector_store

router = APIRouter()

@router.post("/embed")
def embed(uploaded_file: UploadFile):
  # check folder is exists
  if not os.path.exists("./app/storage"):
    os.makedirs("./app/storage")
  
  file = uploaded_file.file
  ext = uploaded_file.filename.split(".")[-1]
  filename = str(uuid4()) + "." + ext
  # save file to `app/storage`
  with open(f"./app/storage/{filename}", "wb") as f:
    f.write(file.read())
  
  if ext == "csv":
    # Load Recipes from CSV
    recipes = CSVLoader(f"./app/storage/{filename}").load_and_split()
    # Add Recipes to Vector Store
    vector_store.add_documents(recipes)
    print(f"\t - Added {filename} to Vector Store")
  elif ext == "json":
    # Load Recipes from JSON
    recipes = JSONLoader(
      f"./app/storage/{filename}",

    ).load_and_split()
    # Add Recipes to Vector Store
    vector_store.add_documents(recipes)
    print(f"\t - Added {filename} to Vector Store")

  return {"message": "File uploaded successfully"}
  