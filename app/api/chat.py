from fastapi import APIRouter
from pydantic import BaseModel 
from typing import List , Optional 
import uuid 
from app.services.redis_service import redis_service
from app.services.database import DatabaseService
from app.services.rag_service import rag_service
import re 



router = APIRouter(prefix="/api", tags=["chat"])


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

      # save user message 
      redis_service.save_mesaage(session_id , "user" , request.message) 
      
      # get history 
      history = redis_service.get_history(session_id)
      history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
       
      # check for interview booking 
      booking_info = extract_booking_info(request.message)
      if booking_info :
            DatabaseService.save_booking (
                  name = booking_info["name"] ,
                  email=booking_info["email"],
                  date=booking_info["date"],
                  time=booking_info["time"]
            )
            bot_reply = f"✅ Interview booked for {booking_info['name']} on {booking_info['date']} at {booking_info['time']}. Details saved in database."
      else : 
           bot_reply = rag_service.generate_response(request.message, history_str) 

      # save bot response 
      redis_service.save_message(session_id , "assistant", bot_reply)
      
     
      return ChatResponse(
            response=bot_reply ,
            session_id=session_id ,
            message_history = history[-10]
      )
def extract_booking_info(text:str) :
      email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
      date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
      time_match = re.search(r'(\d{1,2}:\d{2})', text)  

      if email_match and date_match :
            return {
                  "name" : "candidate" ,
                  "email" : email_match.group() , 
                  "date" : date_match.group() ,
                  "time" : time_match.group() if time_match else "10:00"
            } 
            
      return None 
