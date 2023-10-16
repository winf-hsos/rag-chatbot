import uuid
from unstructured.partition.auto import partition
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from . import EmbeddingModel

import os
import json
import datetime

class KnowledgeBaseDocument:
    def __init__(self, raw_file_name, processed_file_name) -> None:
        self.raw_file_name = raw_file_name
        self.processed_file_name = processed_file_name     
        self.filtered_text_elements = []
        self.chunks = []
        self.chunk_embeddings = []
          
    def save(self):
        with open(self.processed_file_name, 'w') as file:
            json.dump(self.to_json(), file, indent=4)
    
    def load(self):
        pass

    def get_name(self):
        return os.path.basename(self.raw_file_name)

    def split(self, chunk_size=500, chunk_overlap=0):
        # TODO: Split by page break and create separate document for each page
        langchain_document = Document(page_content=self.text, metadata={"id": self.id, "source": f"{self.raw_file_name}"})
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        splits = text_splitter.split_documents([langchain_document])
        #print(splits)
        self.split_documents = [ { "content":  s.page_content, "metadata" : s.metadata } for s in splits]
        
        
        # Create chunk instances
        from .chunk import Chunk
        for split_doc in self.split_documents:
            c = Chunk(split_doc)
            self.chunks.append(c)

        return self.chunks

    def embed_chunks(self, embedding_model: EmbeddingModel):
        chunk_embeddings = embedding_model.embed([c.content for c in self.chunks])
        for i, c in enumerate(self.chunks):
            c.set_embedding(chunk_embeddings["data"][i]["embedding"]) 

    def to_json(self):
        doc_json = { 
            "id" : self.id, 
            "type" : self.type,
            "text_elements" : [str(el) for el in self.text_elements],
            "filtered_text_elements" : [str(el) for el in self.filtered_text_elements],
            "text" : self.text,
            "split_documents" : [str(doc) for doc in self.split_documents],
            "chunks": [c.to_json() for c in self.chunks]
            }

        return doc_json
    
    @staticmethod
    def create_document(document_json_data, raw_file_name, processed_file_name, embedding_model):
        
        doc = None
        if document_json_data["type"] == "text":
            doc = TextKnowledgeBaseDocument(raw_file_name, processed_file_name)
        else:
            print(f"ERROR: Unknown document type: {document_json_data['type']}")
            return None
        
        raw_file_name_stats = os.stat(raw_file_name)
        raw_file_last_changed = datetime.datetime.fromtimestamp(raw_file_name_stats.st_mtime)

        processed_file_name_stats = os.stat(processed_file_name) if os.path.exists(processed_file_name) else None
        processed_file_last_changed = datetime.datetime.fromtimestamp(processed_file_name_stats.st_mtime) if processed_file_name_stats != None else datetime.datetime(2030, 1, 1)
        
        # Check if the processed file exists and if the last change date is newer than the raw file
        if os.path.exists(processed_file_name) & (processed_file_last_changed > raw_file_last_changed):
            print(f"DEBUG: A current processed file >{processed_file_name}< exists -> loading document from file")
            # Load document from json file
            with open(processed_file_name, 'r') as file:
                doc_data = json.load(file)
                doc.id = doc_data.get("id")
                doc.text_elements = doc_data.get("text_elements")
                doc.filtered_text_elements = doc_data.get("filtered_text_elements")
                doc.text = doc_data.get("text")
                doc.split_documents = doc_data.get("split_documents")

                from . import Chunk
                doc.chunks = []
                for c in doc_data.get("chunks"):
                    doc.chunks.append(Chunk(c))
        else:
            print(f"DEBUG: The file >{processed_file_name}< does not exist or is outdated -> creating document from raw file")
            doc.id = uuid.uuid4().hex
            doc.load()
            doc.split()
            doc.embed_chunks(embedding_model)
            doc.save()

        return doc
            

class TextKnowledgeBaseDocument(KnowledgeBaseDocument):

    def __init__(self, raw_file_name, processed_file_name, type = "text") -> None:
        super().__init__(raw_file_name, processed_file_name)
        self.type = "text"
        
    def load(self):
        # Read the raw file and create elements
        self.text_elements = partition(filename=self.raw_file_name)
      
        # Join all elements into one large text
        for text_element in self.text_elements:
            #if isinstance(el, NarrativeText) or isinstance(el, Title) or isinstance(el, Text): #and sentence_count(el.text) > 0:
            self.filtered_text_elements.append(f"{text_element}\n")

        self.text = '\n'.join(self.filtered_text_elements)
        return self.text
    
    


    

