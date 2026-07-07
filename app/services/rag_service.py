# create custom rag 
from app.services.Vector_service import vector_service 
from langchain_groq import ChatGroq
from dotenv import load_dotenv 
import os 

load_dotenv()

class Custom_Rag :
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key = os.getenv("Groq_APi_Key") ,
            model_name = "mixtral-8x7b-32768" ,
            temperature = 0.2 
        )

    def get_relevent_context(self , query:str , limit : int = 3): 
        """Retrieve relevant chunks from Qdrant"""
        try : 
            result = vector_service.client.search(
                collection_name = "documents" ,
                query_vector = vector_service.embeddings.embed_query(query) ,
                limit = limit 
            )
            context = "\n\n".join([hit.playload["text"]for hit in result])
            return context
        except : 
            return " "


    def generate_response(self , query:str , history:list) :

        """custom rag respone""" 
        context = self.get_relevent_context(query)

        prompt = """You are a helpful assistant. Use the following context to answer the question.
If you don't know, say you don't know.

context : {context}

Conversation History:
{history}

Question: {query}

Answer:
"""
        try : 
              response =  self.llm.invoke(prompt)
              return response.context 
        except : 
            return "Sorry, I couldn't generate a response."
        
rag_service = Custom_Rag()
      