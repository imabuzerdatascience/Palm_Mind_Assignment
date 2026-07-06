from fastapi import APIRouter , UploadFile , File 

router = APIRouter (
    prefix= "/upload" , 
    tags= ["Documnet "]
)

@router.post("/") 
async def upload_documnet (
    file : UploadFile = File(...)


) : 
    return {
        "filename" : file.filename , 
        "content_type" : file.content_type
    }