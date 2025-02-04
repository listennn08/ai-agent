from fastapi import APIRouter
from fastapi import UploadFile

router = APIRouter()

@router.get("/embed")
def embed(file: UploadFile):
  pass