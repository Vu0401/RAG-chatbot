import streamlit as st
import tempfile
import os
from chatvpt.rag.file_loader import Loader
from chatvpt.rag.vectordb import VectorDB
from chatvpt.rag.model import get_model_llm
from chatvpt.rag.rag import RAG
from Utils.htmlTemplates import bot_template, user_template, css

def load_pdf(pdf_files):
    loader = Loader()
    temp_dir = tempfile.mkdtemp()
    temp_paths = []
    
    for pdf_file in pdf_files:
        temp_path = os.path.join(temp_dir, pdf_file.name)
        with open(temp_path, "wb") as f:
            f.write(pdf_file.getvalue())
        temp_paths.append(temp_path)
    
    loaded_pdfs = loader.load(temp_paths, workers=4)
    
    for temp_path in temp_paths:
        os.remove(temp_path)
    os.rmdir(temp_dir)
    
    return loaded_pdfs

def main():
    st.set_page_config(page_title="ChatVPT", page_icon=":robot_face:")
    
    st.write(css, unsafe_allow_html=True)  # Add this line to apply CSS

    header_container = st.container()
    with header_container:
        st.header("ChatVPT")
        st.write("Welcome to ChatVPT")
        user_query = st.text_input("Message:")
    
    chat_container = st.empty()  

    if 'rag' not in st.session_state:
        st.session_state.rag = None
        
    if 'history' not in st.session_state:
        st.session_state.history = []
    
   
    if st.button("Clear Chat History"):
        st.session_state.history = []
        st.success("Chat history cleared")

    if user_query:
        if st.session_state.rag is None:
            st.warning("Please submit PDF files!")
        else:
            st.session_state.history.append(("User", user_query))
            ans = st.session_state.rag.rag_chain(st.session_state.history, user_query)
            st.session_state.history.append(("ChatVPT", ans))
    
    with chat_container.container():
        for role, message in st.session_state.history:
            if role == "User":
                st.write(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)
            
    with st.sidebar:
        st.subheader("Docs")
        pdf_docs = st.file_uploader("Upload a PDF file", type=["pdf"], accept_multiple_files=True)
        if st.button("Submit"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF file before pressing Submit.")
            else:
                with st.spinner("Loading..."):
                    chunks = load_pdf(pdf_docs)
            
                    if chunks:
                        vector_db = VectorDB(chunks)
                        retriever = vector_db.get_retriever()

                    if retriever:
                        llm = get_model_llm(model_name="Qwen/Qwen2.5-3B-Instruct", max_new_token=200, temperature=0.5, device="CPU")
                        st.session_state.rag = RAG(llm, retriever)
                
                    st.success(f"Uploaded {len(pdf_docs)} PDF files successfully!")
    
if __name__ == "__main__":
    main()