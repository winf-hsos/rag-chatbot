import sys
import os
os.environ["CHATBOT_CONFIG"] = "C:/code/rag-chatbot/chatbot/config.yaml"
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory)

import chatbot as cb

qa_bot = cb.QABot("Willy")

stats = qa_bot.get_stats()
#print(stats)

question = input("User: ")
while question != "exit":
    
    answer = qa_bot.ask(question)
    print(f"{qa_bot.name}: {answer.get_text()}")
    #print(answer.to_json())

    # Next question
    question = input("User: ")