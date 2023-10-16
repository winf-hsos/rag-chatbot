import streamlit as st
import sys
sys.path.append("C:\\code\\rag-chatbot")
import chatbot as cb

st.title("Q&A Bot")
st.caption("A Q&A bot developed at the [University of Applied Sciences Osnabrück](http://hs-osnabrueck.de/).")

qa_bot = cb.QABot("Philipp") if st.session_state.get("qa_bot") is None else st.session_state.get("qa_bot")
st.session_state["qa_bot"] = qa_bot

refresh = st.button("Refresh bot")
if refresh:
    qa_bot = cb.QABot("Philipp")
    st.session_state["qa_bot"] = qa_bot

query_text = st.text_input('Please enter your question:')

if query_text:
    answer = qa_bot.ask(query_text)

    with st.chat_message('assistant'):
        st.write(answer.get_text())

    if answer:
        st.header("Answer Details")
        answer_details = st.expander("Answer details", expanded=True)
        with answer_details:
            st.write(answer.to_json())

st.header("Bot Statistics")
stats = st.expander("Stats", expanded=True)
with stats:
    st.write(qa_bot.get_stats())