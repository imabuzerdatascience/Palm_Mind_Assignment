from fastapi import APIRouter
from pydantic import BaseModel 
from typing import List , Optional 
import uuid 
from app.services.redis_service import redis_service
from langchain_groq import ChatGroq 
from dotenv import load_dotenv 
import os 

load_dotenv()

router = APIRouter(prefix="/api", tags=["chat"])


class ChatMessage(BaseModel) :
    message : str 
    session_id : Optional[str] = None 

class ChatResponse(BaseModel) :
        response : str 
        session_id : str 
        mesaage_history : List[dict] 

# LLm Setup (GROQ)
llm = ChatGroq(
      groq_api_key = os.getenv("Groq_APi_Key") ,
      model_name = "mixtral-8x7b-32768" ,
      temperature = 0.7
)


@router.post("/chat")
async def chat_endpoint (request:ChatMessage) :
      
      session_id = request.session_id or str(uuid.uuid4()) 

      # save user message 
      redis_service.save_mesaage(session_id , "user" , request.message) 
      
      # get history 
      history = redis_service.get_history(session_id)

       # create prompt with history 
      prompt = "You are a helpful assitant . Answer the question based on previous conversion " 
      for msg in history : 
            prompt += f"{msg["role"]}{msg["content"]}\n" 
      promt += f"user : {request.message}\nassistant"
       
      # get response from llm 
      try : 
            response = llm.invoke(prompt)
            bot_reply = response.content 
      except Exception as e : 
            bot_reply = "Sorry , I have trouble responding right now" 

      # save bot response 
      redis_service.save_message(session_id , "assistant", bot_reply)
      

     
      return ChatResponse(
            response=bot_reply ,
            session_id=session_id ,
            message_history = history[-10]
      )
