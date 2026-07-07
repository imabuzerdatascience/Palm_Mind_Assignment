# create custom rag 
from app.services.Vector_service import vector_service 
from langchain_groq import ChatGroq
from dotenv import load_dotenv 
import os 

load_dotenv()

class Custom_Rag :
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key = os.getenv("Groq_APi_Key") 
            model_name = "mixtral-8x7b-32768"
            temperature = 0.2 
        )

       
      