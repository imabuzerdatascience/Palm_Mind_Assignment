from fastapi import FastAPI 
from app.api.upload import router as upload_router 

app = FastAPI(
    title = "Palm_mind",

) 

app.include_router(upload_router)