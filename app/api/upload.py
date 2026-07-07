from fastapi import APIRouter , UploadFile , File , HTTPException
from pydantic import BaseModel
import shutil
import os 
from app.utils.chunkers import get_chunk
from app.services.Vector_databse import vector_service 
from langchain_community.document_loaders import PyPDFLoader , TextLoader

router = APIRouter (
    prefix= "/api" , 
    tags= ["upload"]
)

Uploads_dir = "uploads"
os.makedirs(Uploads_dir , exist_ok=True)

vector_service = vector_service() 

# For error handling 
class UploadRequest(BaseModel):
    chunk_strategy : str = "fixed"
    chunk_size : int = 500 
    chunk_overlap : int = 50

# For error handling 
class UploadResponse(BaseModel):
    message : str 
    filename : str 
    file_size : int 
    status : str = "success"

@router.post("/upload") 
async def upload_document (
    file : UploadFile = File(...) , request = UploadRequest
    ): 
    
    if request is None : 
        request = UploadRequest()

    if not file.filename.lower().endswith((".pdf" , ".txt")) :
        raise HTTPException(status_code=400 , detail="only PDF and TXT are aloowed ")
    
    file_path = os.path.join(Uploads_dir , file.filename)


    try : 
        # save file 
        file_path = os.path.join(Uploads_dir , file.filename)

        with open(file_path, "wb") as buffer : 
            shutil.copyfileobj(file.file, buffer) 

        # Text Extraction
        if file.filename.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path, encoding="utf-8")
        
        documents = loader.load()

        # Chunking
        text_splitter = get_chunk(
            strategy=request.chunk_strategy,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        chunks = text_splitter.split_documents(documents)

        # Store in Qdrant
        document_id = vector_service.store_chunks(chunks, file.filename)

        return UploadResponse(
            message="Document successfully processed and stored in Qdrant",
            document_id=document_id,
            chunks_count=len(chunks),
            chunk_strategy=request.chunk_strategy
        )
    except Exception as e : 
        raise HTTPException(status_code = 500 , detail = f"upload failed:{str(e)}")


  



 



  