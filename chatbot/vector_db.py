import chromadb
import chromadb.config

class VectorDatabase:

     def __init__(self, knowledge_base) -> None:
          self.knowledge_base = knowledge_base
          self.engine = "ChromaDB"
          self.db_client = chromadb.Client(settings=chromadb.config.Settings(allow_reset=True))
          self.db_client.reset()
          self.db_client.create_collection("documents")
          self.collection = self.db_client.get_collection("documents")

          self._setup()

     def _setup(self):
          docs = self.knowledge_base.docs
          #print(docs)
          for doc in docs:
               for i, c in enumerate(doc.chunks):
                    self.add_document(f"{doc.id}_{i}", c.content, c.embedding, c.metadata)
               
     def add_document(self, id, doc, embedding, metadata):
          self.collection.add(
               documents=[doc],
               embeddings=[embedding],
               metadatas=[metadata],
               ids=[id]
    )
          
     def query(self, query_prompt_embedding, n_results=2):
          results = self.collection.query(
               query_embeddings=[query_prompt_embedding],
               n_results=n_results,
               include=["distances", "documents", "metadatas"]
          ) 
          return results

     def get_stats(self):
          db_data = self.collection.get()
          return {
               "engine" : self.engine,
               "num_document_chunks" : len(db_data["ids"])
          }