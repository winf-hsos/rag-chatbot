import json
import os

class KnowledgeBase:

     PROCESSED_DIR = "processed_documents"
     RAW_DIR = "raw_documents"
     KNOWLEDGE_BASE_INDEX_FILE = "knowledge_base.json"

     def __init__(self, embedding_model) -> None:
          self.embedding_model = embedding_model

          from . import KNOWLEDGE_BASE_ROOT
          from . import KNOWLEDGE_BASE_AUTO_SYNC
          self.root = KNOWLEDGE_BASE_ROOT
          self.raw_dir = os.path.join(self.root, KnowledgeBase.RAW_DIR)
          self.processed_dir = os.path.join(self.root, KnowledgeBase.PROCESSED_DIR)
          self.auto_sync = KNOWLEDGE_BASE_AUTO_SYNC
          self.docs = []

          self._setup()

     def _setup(self):

          from .doc import KnowledgeBaseDocument, TextKnowledgeBaseDocument
          
          # Step 1: Read knowledge base JSON file
          knowledge_json_file = os.path.join(self.root, KnowledgeBase.KNOWLEDGE_BASE_INDEX_FILE)
          with open(knowledge_json_file, 'r') as file_json_data:
               knowledge_base_json_data = json.load(file_json_data)
               self.db_index = knowledge_base_json_data
               #print(knowledge_base_data)

          # Step 2: If auto-add is enabled, add any raw files not in the knowledge base yet
          if self.auto_sync == True:
               print(f"Auto-sync is enabled --> looking for any new or removed files and synchronize knowledge base index.")
               self._auto_add_new_files()
               self._auto_delete_removed_files()
               self._save_index()
         
          # Step 2: Create documents from the index file
          for file_json_data in self.db_index["files"]:
               # Depending on whether the processed file exists, and when the document was last changed, 
               # the document will be processed or loaded from the existing json file
               raw_file_name = os.path.join(self.root, KnowledgeBase.RAW_DIR, file_json_data["name"])
               processed_file_name = os.path.join(self.root, KnowledgeBase.PROCESSED_DIR, f'{file_json_data["name"]}.json')

               new_doc = KnowledgeBaseDocument.create_document(file_json_data, raw_file_name, processed_file_name, self.embedding_model)
               if new_doc != None:
                    self.docs.append(new_doc) 

          print(f"DEBUG: Knowledge base setup complete. Found {len(self.docs)} documents.")

     def _auto_add_new_files(self):
          # Walk through the root directory tree recursively
          # and check for files that are not in the index yet
          for folder_path, _, file_names in os.walk(self.raw_dir):
               for file_name in file_names:
                    # Get the full path of the file
                    full_path = os.path.join(folder_path, file_name)
                    
                    # Calculate the relative path from the root folder
                    relative_path = os.path.relpath(full_path, start=self.raw_dir)

                    # Check if this file is already in the knowledge base index file
                    exists = any(f["name"] == relative_path for f in self.db_index["files"])

                    if exists == True:
                         print(f"DEBUG: The file {relative_path} is already in the index.")
                    else:
                         print(f"DEBUG: The file {relative_path} is not yet in the index.")
                         self._add_file_to_index(relative_path, full_path)
     
     def _add_file_to_index(self, relative_path, full_path):
          import magic 
          mime_type = magic.from_file(full_path, mime=True)
          print(mime_type)
          self.db_index["files"].append({
               "name": relative_path,
               "path": full_path,
               "type": mime_type
          })	

     def _auto_delete_removed_files(self):
          # Walk through the index files and check if the file exists
          # if not, remove it from the index
          for file_json_data in self.db_index["files"]:
               full_path = os.path.join(self.raw_dir, file_json_data["name"])
               exists = os.path.exists(full_path)
               if exists == False:
                    print(f"DEBUG: The raw file {file_json_data['name']} does not exist anymore. Removing from index.")
                    self.db_index["files"].remove(file_json_data)

     def _save_index(self):
          knowledge_json_file = os.path.join(self.root, KnowledgeBase.KNOWLEDGE_BASE_INDEX_FILE)
          with open(knowledge_json_file, 'w') as file_json_data:
               json.dump(self.db_index, file_json_data, indent=4)

     def get_documents(self):
          return self.docs
     
     def get_stats(self):
          stats = { 
               "num_total_documents" : len(self.docs)
               }
          return stats
     