from fastapi import APIRouter
from pydantic import BaseModel 
from typing import List , Optional 
import uuid 

router = APIRouter(prefix="/api", tags=["chat"])

chat_session = {}

class ChatMessage(BaseModel) :
    message : str 
    session_id : Optional[str] = None 

class ChatResponse(BaseModel) :
        response : str 
        session_id : str 
        mesaage_history : List[dict] 

@router.post("/chat")
async def chat_endpoint (request:ChatMessage) :
      
      session_id = request.session_id or str(uuid.uuid4()) 

      if session_id not in chat_session :
            chat_session[session_id] = []

      chat_session[session_id].append({"role":"user" , "content":request.message })

      bot_reply = f"Received your message: '{request.message}'. This is a simple response. (Session: {session_id[:8]}...)"

      chat_session[session_id].append({"role":"assistant" , "content": bot_reply })

     
      return ChatResponse(
            response=bot_reply ,
            session_id=session_id ,
            message_history = chat_session[session_id][-6:]
      )
