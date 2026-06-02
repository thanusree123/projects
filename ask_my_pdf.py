import os
import warnings
# This line safely mutes the deprecation warnings so your screen stays clean!
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def run_rag_pipeline():
    # 1. DOCUMENT LOADING & PARSING
    print("🔄 Step 1: Loading raw document...")
    if not os.path.exists("sample.txt"):
        with open("sample.txt", "w") as f:
            f.write(
                "Company Return Policy:\n"
                "Customers can return any defective or damaged products within 30 days of purchase.\n"
                "To initiate a return, please email support@company.com with your order receipt.\n\n"
                "Office Working Hours:\n"
                "Our physical office is open Monday through Friday, from 9:00 AM to 5:00 PM EST."
            )
    
    loader = TextLoader("sample.txt")
    raw_documents = loader.load()
    print(f"✅ Successfully loaded source document.\n")

    # 2. TEXT CHUNKING (SLICING)
    print("🔄 Step 2: Chopping text into overlapping chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)
    chunks = text_splitter.split_documents(raw_documents)
    print(f"✅ Created {len(chunks)} small text chunks.\n")

    # 3. EMBEDDINGS (WORDS TO MATH)
    print("🔄 Step 3: Initializing the Hugging Face mathematical model...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    print("✅ Embedding model is ready.\n")

    # 4. VECTOR DATABASE (STORING COORDINATES)
    print("🔄 Step 4: Computing coordinates and saving to Vector DB...")
    db_folder = "./my_chroma_db"
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=db_folder
    )
    print(f"✅ Vector database successfully saved locally in folder: '{db_folder}'\n")

    # TESTING THE RETRIEVAL PIPELINE
    print("🚀 PIPELINE COMPLETE. Testing database search...")
    query = "How do I return a damaged product?"
    print(f"Question asked: '{query}'")
    
    matching_chunks = vector_db.similarity_search(query, k=1)
    
    print("\n--- 🔍 SEARCH RESULT FOUND ---")
    for doc in matching_chunks:
        print(f"Text content: {doc.page_content}")
        print("-" * 50)

if __name__ == "__main__":
    run_rag_pipeline()