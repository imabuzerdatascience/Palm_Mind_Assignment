import redis 
import json 
from typing import List , Dict , Optional 
import os 
from dotenv import load_dotenv 

load_dotenv() 


class Redis_Service() :
    def __init__(self):
      self.redis_client = redis.Redis(
         host = "localhost" ,
         port = 6379 , 
         decode_responses=True , 
         socket_connect_timeout = 5 
      )

      self.session_prefix = "chat"
   

# save message 
    def save_message(self , session_id: str,role:str , content:str):
       """save message in chat history""" 
       key = f"{self.session_prefix}{session_id}" 

       message = {
          "role" : role , 
          "content " : content , 
          "timestamp" : str(os.times()[4])
       }
       
       self .redis_client.rpush(key, json.dumps(message))
       self.redis_client.ltrim(key, -20 , -1)

    def get_history(self , session_id:str)-> List[Dict] :
       key = f"{self.session_prefix}{session_id}"
       messages = self.redis_client.lrange(key , 0 , -1)
       return [json.loads(msg)for msg in messages] 
    
    def clear_history(self , session_id : str) :
       key = f"{self.session_prefix}{session_id}"
       self.redis_client.delete(key)


redis_service = Redis_Service()