from fastapi import APIRouter , UploadFile , File , HTTPException
from pydantic import BaseModel
import shutil
import os 


router = APIRouter (
    prefix= "/api" , 
    tags= ["upload"]
)

Uploads_dir = "uploads"
os.makedirs(Uploads_dir , exist_ok=True)


# For error handling 
class UploadResponse(BaseModel):
    message : str 
    filename : str 
    file_size : int 
    status : str = "success"

@router.post("/upload") 
async def upload_document (
    file : UploadFile = File(...)): 

    if not file.filename.lower().endswith((".pdf" , ".txt")) :
        raise HTTPException(status_code=400 , detail="only PDF and TXT are aloowed ")
    
    try : 
        # save file 
        file_path = os.path.join(Uploads_dir , file.filename)

        with open(file_path, "wb") as buffer : 
            shutil.copyfileobj(file.file, buffer) 

        file_size = os.path.getsize(file_path)

        return UploadResponse(
            message= "File uploaded successfully" ,
            filename = file.filename , 
            file_size = file_size 
        )
    except Exception as e : 
        raise HTTPException(status_code = 500 , detail = f"upload failed:{str(e)}")


  



 



  