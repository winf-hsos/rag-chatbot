class Answer:
    
    def __init__(self):
        self.answer_text = ""
        self.retrieved_documents = []
        self.openai_answer = None

    def set_openai_answer(self, answer_json):
        self.openai_answer = answer_json
        self.answer_text = answer_json['choices'][0]['message']['content']

    def set_retrieved_documents(self, documents):
        self.retrieved_documents = documents

    def set_generated_prompt(self, prompt):
        self.generated_prompt = prompt

    def set_message_history(self, messages):
        self.message_history = messages

    def get_text(self):
        return self.answer_text
    
    def to_json(self):
        return {
            "answer_text": self.answer_text,
            "retrieved_documents": self.retrieved_documents,
            "generated_prompt": self.generated_prompt,
            "message_history": self.message_history,
            "openai_answer": self.openai_answer
        }

    def __str__(self):
        return f"{self.answer_text}"

    
    

