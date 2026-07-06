from fastapi import FastAPI 
from app.api.upload import router as upload_router 

app = FastAPI(
    title = "Palm_mind",

) 

#include routers
app.include_router(upload_router)


@app.get("/") 
async def root():
    return {"Backend is runing"}