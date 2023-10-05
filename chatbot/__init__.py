from chatbot.qa_bot import QABot
from chatbot.embedding_model import EmbeddingModel
from chatbot.llm import LargeLanguageModel
from chatbot.knowledge_base import KnowledgeBase
from chatbot.vector_db import VectorDatabase

import os
import sys

if "CHATBOT_CONFIG_FILE" in os.environ:
    chatbot_config_file = os.environ.get("CHATBOT_CONFIG_FILE")
else:
    print("ERROR: environment variable CHATBOT_CONFIG_FILE is not set.")
    sys.exit(0)

import yaml
with open(chatbot_config_file, 'r') as f:
    config = yaml.safe_load(f)

OPENAI_API_KEY = config.get("openai_api_key")
