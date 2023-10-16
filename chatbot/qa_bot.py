from chatbot.embedding_model import EmbeddingModel
from chatbot.knowledge_base import KnowledgeBase
from chatbot.llm import LargeLanguageModel
from chatbot.vector_db import VectorDatabase
from chatbot.answer import Answer

class QABot:

    def __init__(self, name) -> None:
        self.name = name

        self.embedding_model = None
        self.knowledge_base = None
        self.vector_db = None
        self.llm = None

        self.setup()
        
        
    def setup(self):

        # Step 1: Create Embedding Model
        self.embedding_model = EmbeddingModel()

        # Step 2: Create Knowledge Base
        self.knowledge_base = KnowledgeBase(self.embedding_model)

        # Step 3: Create Vector DB
        self.vector_db = VectorDatabase(self.knowledge_base)

        # Step 4: Create LLM
        self.llm = LargeLanguageModel()


    def ask(self, question) -> Answer:

        # Step 1: Get similar documents from vector db
        similar_docs = self._query_db(question)
        #print(similar_docs)

        # Step 2: Generate prompt
        prompt = self._generate_prompt(question, similar_docs)

        # Step 3: Complete prompt using LLM
        messages=[
            {"role": "system", "content": f"You are {self.name}, a helpful assistant and always kind."},
            {"role": "user", "content": prompt}
        ]

        llm_answer = self.llm.complete(messages)

        answer = Answer()
        answer.set_retrieved_documents(similar_docs)
        answer.set_generated_prompt(prompt)
        answer.set_message_history(messages)
        answer.set_openai_answer(llm_answer)

        return answer
  
    def _query_db(self, query_prompt):
        # Embed query prompt
        query_embedding = self.embedding_model.embed(query_prompt)
        similar_docs = self.vector_db.query(query_embedding["data"][0]["embedding"], n_results=3)
        return similar_docs
    
    def _generate_prompt(self, question, similar_docs):

        # Create a string from the documents
        doc_string = ""
        for doc in similar_docs["documents"][0]:
            doc_string += doc + "\n"

        prompt_template = f"""Consider only the following context to answer the question below. Always answer in German. Keep your answers short and precise. Do not make up answers, if the information is not in the context, just say "Das weiß ich leider nicht".\n\nContext: "{doc_string}"\n\nQuestion: "{question}"\n\nHelpful answer: """

        return prompt_template


    def get_vector_db(self):
        return self.vector_db 
    
    def get_llm(self) -> LargeLanguageModel:
        return self.llm
    
    def get_stats(self):
        stats = { "name" : self.name, "type" : "QABot" }
        stats["embedding_model"] = self.embedding_model.get_stats()
        stats["knowledge_base"] = self.knowledge_base.get_stats()
        stats["vector_database"] = self.vector_db.get_stats()
        
        return stats