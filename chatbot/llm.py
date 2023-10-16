class LargeLanguageModel:

    def __init__(self, model_name = "gpt-3.5-turbo") -> None:
        self.model_name = model_name

    def complete(self, messages):
        from . import OPENAI_API_KEY
        import openai
        openai.api_key = OPENAI_API_KEY

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response

    



