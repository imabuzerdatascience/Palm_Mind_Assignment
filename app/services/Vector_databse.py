from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct 
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings   
import uuid
from datetime import datetime
from typing import List

