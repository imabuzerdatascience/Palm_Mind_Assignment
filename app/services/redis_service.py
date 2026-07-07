import redis 
import json 
from typing import List , Dict , Optional 
import os 
from dotenv import load_dotenv 

load_dotenv() 


class Redis_Service() :
    def __init__(self):
      self.redis.client = redis.Redis(
         host = "localhost" 
         port = 6379 , 
         decode_response = True
      )

      self.session_prefix = "chat session"
   

# save message 
    def save_message(self , session_id: str,role:str , content:str):
       """save message in chat history""" 
       key = f"{self.session_prefix}{session_id}" 

       message = {
          "role" : role , 
          "content " : content , 
          "timestamp" : str(os.times()[4])
       }
