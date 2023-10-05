from chatbot.llm import LargeLanguageModel

class QABot:

    def __init__(self, name) -> None:
        self.name = name
        self.knowledge_base = None
        self.vector_db = None
        self.embedding_model = None
        self.llm = None
        
        pass

    def ask(self, question):
        return f"My name is {self.name}. Unfortunately, I am not yet implemented 😥. So go and google your question: {question}"

    def get_vector_db(self):
        return self.vector_db 
    
    def get_llm(self) -> LargeLanguageModel:
        return self.llm
