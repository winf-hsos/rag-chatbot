import streamlit as st
import os
import sys
sys.path.append("C:\\code\\rag-chatbot")
import chatbot as cb


st.title("Knowledge Base")
st.caption("On this page, you can manage the documents for your personal knowledge base.")

qa_bot = cb.QABot("Philipp") if st.session_state.get("qa_bot") is None else st.session_state.get("qa_bot")
st.session_state["qa_bot"] = qa_bot

files_in_directory = os.listdir(f"{cb.KNOWLEDGE_BASE_ROOT}\\raw_documents")
st.metric("Number of files", len(files_in_directory) )

docs = qa_bot.knowledge_base.get_documents()


#st.write("Files in the selected directory:")
#st.write(files_in_directory)

#for file_name in files_in_directory:
    #st.write(f"- {file_name}")

# Create checkboxes for each file
#selected_files = st.multiselect("Select file(s) to delete:", files_in_directory)
#delete = st.button("Delete files", type = 'secondary')
#if delete:
    #for file_name in selected_files:
     #   os.remove(f"{cb.KNOWLEDGE_BASE_ROOT}\\raw_documents\\{file_name}")
    #st.toast("The selected files have been deleted.")

# Display selected files
#st.write("Selected files:")
#st.write(selected_files)