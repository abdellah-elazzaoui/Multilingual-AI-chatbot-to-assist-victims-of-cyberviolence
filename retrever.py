from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

# ============ CONFIG ============
PDF_DIRECTORY = "data/knowledge_base"
DB_LOCATION = "data/chromadb"
COLLECTION_NAME = "emc_helpline"

print(" Initializing System...")

# Load embeddings (supports both Arabic & French)
embed = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={'normalize_embeddings': True}
)

# Load vector store
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_LOCATION,
    embedding_function=embed
)

# ============ LOAD & SPLIT ============
def load_and_split():
    """Load all PDFs and split into chunks"""
    # Load PDFs
    loader = DirectoryLoader(
        PDF_DIRECTORY,
        glob="**/*.pdf",  
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    docs = loader.load()
    
    if not docs:
        print(" No PDFs found!")
        return []
    
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    
    # Add metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata['chunk_id'] = i
        chunk.metadata['source'] = os.path.basename(chunk.metadata['source'])
    
    print(f"Loaded {len(docs)} pages → {len(chunks)} chunks")
    return chunks

# ============ INDEX ============
def index_pdfs():
    """Index all PDFs into vector database"""
    chunks = load_and_split()
    
    if not chunks:
        return

    if os.path.exists(DB_LOCATION):
        import shutil
        shutil.rmtree(DB_LOCATION)
        print("🗑️ Removed old database")
    
    # Add to vector store
    vector_store.add_documents(chunks)
    vector_store.persist()
    print(f"Indexed {len(chunks)} chunks successfully!")

# ============ SEARCH ============
def search(query, k=5):
    """Search for similar documents"""
    results = vector_store.similarity_search(query, k=k)
    
    print(f"\n🔍 Found {len(results)} results for: '{query}'\n")
    for i, doc in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(f" Source: {doc.metadata.get('source', 'Unknown')}")
        print(f" Content: {doc.page_content[:200]}...")
        print()

# ============ MAIN ============
if __name__ == "__main__":
    print("\n" + "="*50)
    print(" PDF KNOWLEDGE BASE (Arabic/French)")
    print("="*50 + "\n")
    
    while True:
        print("\nMENU:")
        print("1. Index PDFs")
        print("2. Search")
        print("3. Exit")
        
        choice = input("\nChoose (1-3): ")
        
        if choice == '1':
            index_pdfs()
            
        elif choice == '2':
            query = input("🔍 Enter your question (in Arabic or French): ")
            k = int(input("Number of results (default 5): ") or "5")
            search(query, k)
            
        elif choice == '3':
            print(" Goodbye!")
            break
        else:
            print(" Invalid choice")