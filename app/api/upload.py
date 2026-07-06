from fastapi import APIRouter , UploadFile , File , HTTPException
from pydantic import BaseModel
from typing import Optional
import shutil
import os 
from datetime import datetime 

router = APIRouter (
    prefix= "/upload" , 
    tags= ["Documnet "]
)

Uploads_dir = "uploads"
os.makedirs(Uploads_dir , exist_ok=True)


# For error handling 
class UploadResponse(BaseModel):
    message : str 
    filename : str 
    file_size : int 
    status = "success"

@router.post("/upload") 
async def upload_documnet (
    file : UploadFile = File(...)


) :