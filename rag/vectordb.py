from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class VectorDB:
    def __init__(self, chunks):
        self.chunks = chunks
        self.embedding = HuggingFaceEmbeddings()
        self.vector_db = self._create_vectordb(chunks)
        
    def _create_vectordb(self, chunks):
        vector_db = Chroma.from_documents(chunks, embedding=self.embedding)
        return vector_db

    def get_retriever(self, 
                      search_type: str = "similarity", 
                      search_kwargs: dict = {"k": 5}
                      ):
        retriever = self.vector_db.as_retriever(search_type=search_type,
                                         search_kwargs=search_kwargs)
        return retriever

    
