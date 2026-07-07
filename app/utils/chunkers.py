from langchain_text_splitters import RecursiveCharacterTextSpliter , CharacterTextSplitter 

def get_chunk(strategy: str="fixed" , chunk_size : int =500 , chunk_overlap :int = 50) :

    # two chunk strategies 
    if strategy.lower() == "recursive" :
        return RecursiveCharacterTextSpliter (
            chunk_size = chunk_size ,
            chunk_overlap = chunk_overlap ,
            seprators = ["/n /n" ,"/n/n" , ".","!","," , "?" , "",""]
        ) 
    else :
        return CharacterTextSplitter(
          chunk_size = chunk_size ,
            chunk_overlap = chunk_overlap    
        )
    