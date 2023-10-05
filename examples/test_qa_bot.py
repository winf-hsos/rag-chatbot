import sys
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory)

import chatbot as cb

qa_bot = cb.QABot("Willy")