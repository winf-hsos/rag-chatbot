import streamlit as st
import os
import sys
sys.path.append("C:\\code\\rag-chatbot")

import chatbot as cb

st.title("Q&A Bot")
st.caption("A Q&A bot developed at the [University of Applied Sciences Osnabrück](http://hs-osnabrueck.de/).")

qa_bot = cb.QABot("Willy")

query_text = st.text_input('Please enter your question:')

if query_text:
    answer = qa_bot.ask(query_text)

    with st.chat_message('assistant'):
        st.write(answer)