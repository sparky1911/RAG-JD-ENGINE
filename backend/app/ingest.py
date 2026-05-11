from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


BASE_DIR = Path(__file__).resolve().parent

PDF_PATH = BASE_DIR / "resume" / "resume.pdf"
COLLECTION_NAME="resume_rag"
QDRANT_URL="http://qdrant:6333"


def load_pdf():
    loader=PyPDFLoader(
        str(PDF_PATH)
    )
    docs=loader.load()
    return docs


def split_documents(docs):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)
    return chunks

def get_embedding_model():
    embedding=HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )
    return embedding


def store_in_qdrant(chunks, embeddings):

    client = QdrantClient(
        url=QDRANT_URL,
        prefer_grpc=False
    )

    if not client.collection_exists(
        COLLECTION_NAME
    ):

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )

    vector_store.add_documents(
        chunks
    )

    return vector_store


def ingest_resume():

    print("Loading PDF...")

    docs = load_pdf()

    print(f"Loaded {len(docs)} pages")

    print("Splitting documents...")

    chunks = split_documents(docs)

    print(f"Created {len(chunks)} chunks")

    print("Loading embedding model...")

    embeddings = get_embedding_model()

    print("Storing vectors in Qdrant...")

    store_in_qdrant(
        chunks,
        embeddings
    )

    print("Resume indexed successfully")


if __name__ == "__main__":

    ingest_resume()
