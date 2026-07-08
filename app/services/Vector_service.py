from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct 
from langchain_community.embeddings import HuggingFaceEmbeddings   
import uuid
from datetime import datetime
from typing import List
from app.services.database import db_service

class VectorService :
    def __init__(self):
        self.client = QdrantClient(path="./qdrant_data")
        self.collection_name = "documnets" 

        # using HugginfaceEmbedding 
        self.embedding = HuggingFaceEmbeddings(
            model_name = "sentence-transformers/all-MiniLM-L6-v2", 

        )
    def create_collection(self): 
        try :
            self.client.get_collection(self.collection_name)
        except :
            self.client.create_collection (
                collection_name = self.collection_name  ,
                vectors_config = VectorParams(size=384 , distance=Distance.COSINE) 
            )
    

# store chunks 
    def store_chunks(self, chunks: List, filename: str):
        self.create_collection()

        document_id =str(uuid.uuid4())
        embedded_chunks = self.embedding.embed_documents(
    [chunk.page_content for chunk in chunks]
) 

        points = [ 
            PointStruct (
                id = str(uuid.uuid4()) ,
                vector = vector , 
                payload = {
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": i,
                    "text": chunks[i].page_content,
                    "upload_time": datetime.now().isoformat()
                }
            )
            for i, vector in enumerate(embedded_chunks)

        ]
        
        self.client.upsert(
    collection_name=self.collection_name,
    points=points
)

        # save meta data in MYSQL
        db_service.save_document_metadata(document_id , filename)

        return document_id 
    

vector_service = VectorService()
