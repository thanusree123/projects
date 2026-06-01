import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

# Page layout configurations
st.set_page_config(page_title="Local PDF RAG Brain", layout="wide")
st.title("📂 Local PDF Research Assistant (RAG)")
st.write("Upload a PDF, let the system embed it locally, and ask your questions.")

# Create an absolute path for database persistence
DB_DIR = os.path.join(os.getcwd(), "chroma_db")

# Initialize our Local Models (Using Ollama)
# Make sure you have run 'ollama run llama3' in your terminal first!
@st.cache_resource
def load_models():
    embeddings = OllamaEmbeddings(model="llama3")
    llm = Ollama(model="llama3")
    return embeddings, llm

embeddings_model, llm_model = load_models()

# Layout split: Left side for upload, Right side for chat
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Document Ingestion")
    uploaded_file = st.file_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Save file to disk temporarily to load it
        temp_file_path = os.path.join(os.getcwd(), "temp_uploaded.pdf")
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())
            
        st.success("File uploaded successfully!")
        
        # Trigger Document Processing Pipeline
        if st.button("🔄 Process & Index PDF"):
            with st.spinner("Parsing text, generating embeddings, and indexing..."):
                # 1. Parsing
                loader = PyPDFLoader(temp_file_path)
                docs = loader.load()
                
                # 2. Chunking (500 character chunks with 50 character overlap)
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                chunks = text_splitter.split_documents(docs)
                
                # 3 & 4. Embedding & Storing into local VectorDB
                vector_db = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings_model,
                    persist_directory=DB_DIR
                )
                st.success(f"Indexed successfully! Split into {len(chunks)} distinct chunks.")
                st.session_state["db_ready"] = True
                
        # Clean up temporary file safely
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

with col2:
    st.header("Ask Your Document")
    user_query = st.text_input("Enter your question based on the document:")
    
    if user_query:
        # Check if the database has been constructed
        if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
            with st.spinner("Searching memory and generating answer..."):
                # Load the persisted vector database
                db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings_model)
                
                # Semantic Search: Retrieve the top 3 closest chunks (k=3)
                retrieved_docs = db.similarity_search(user_query, k=3)
                
                # Extract the raw text from the context results
                context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
                
                # Construct the Augmented Prompt Structure
                augmented_prompt = f"""
                You are a precise assistant analyzing a document. Answer the question using ONLY the provided context below.
                If you do not know the answer based on the context, say explicitly that it is not mentioned in the document.

                Context:
                {context_text}

                Question: {user_query}
                Answer:
                """
                
                # Generate Answer via the local LLM inference engine
                response = llm_model.invoke(augmented_prompt)
                
                # Display Results
                st.markdown("### Answer:")
                st.write(response)
                
                # Visual Transparency: Show the user exactly what was retrieved
                with st.expander("👀 View Raw Retrieved Sources"):
                    for idx, doc in enumerate(retrieved_docs):
                        st.markdown(f"**Source Chunk {idx+1} (Page {doc.metadata.get('page', 'Unknown')}):**")
                        st.info(doc.page_content)
        else:
            st.warning("Please process and index a PDF document on the left before submitting a question.")