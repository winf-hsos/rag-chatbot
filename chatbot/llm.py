class LargeLanguageModel:

    def __init__(self, model_name = "gpt-3.5-turbo") -> None:
        self.model_name = model_name

    def complete(self, messages):
        prompt = self.generate_prompt()

        # Send prompt to openai
        # ...

        pass

    def generate_prompt(self, context, question):
        return "Not implemented yet"
    



