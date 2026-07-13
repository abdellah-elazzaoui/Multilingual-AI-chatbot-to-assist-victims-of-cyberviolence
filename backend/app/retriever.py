from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

# ============ CONFIG ============
PDF_DIRECTORY = "data/knowledge_base"
DB_LOCATION = "data/chromadb"
COLLECTION_NAME = "emc_helpline"
TOP_K = 5

print("Initializing System...")

embed = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={'normalize_embeddings': True}
)

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_LOCATION,
    embedding_function=embed
)

# ============ LOAD & SPLIT ============
def load_and_split():
    """Load all PDFs and split into chunks"""
    if not os.path.isdir(PDF_DIRECTORY):
        print(f" PDF directory not found: {PDF_DIRECTORY}")
        return []

    loader = DirectoryLoader(
        PDF_DIRECTORY,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    docs = loader.load()

    if not docs:
        print(" No PDFs found ")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata['chunk_id'] = i
        chunk.metadata['source'] = os.path.basename(chunk.metadata['source'])

    print(f"Loaded {len(docs)} pages → {len(chunks)} chunks")
    return chunks


# ============ INDEX ============
def index_pdfs():
    """Index all PDFs into the vector database (only if not already indexed)"""
    existing_count = vector_store._collection.count()

    if existing_count > 0:
        print(f"Database already contains {existing_count} chunks. Skipping indexing.")
        return

    chunks = load_and_split()

    if not chunks:
        print("Nothing to index.")
        return

    vector_store.add_documents(chunks)
    print(f"Indexed {len(chunks)} chunks successfully")

index_pdfs()

retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K})