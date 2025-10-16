from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import argparse
import os
import dotenv
import json
from tqdm import tqdm

dotenv.load_dotenv()  # Load environment variables from .env file

# Initialize the embedding model once
embedding_model = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_EMBEDDINGS"),
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION_EMBEDDINGS"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY_EMBEDDINGS"),
)
def embed_text(text: str):
    """Generate embeddings for the given text using Azure OpenAI."""
    response = embedding_model.embed_query(text)
    return response

def embed_jsonl_file(file_path: str):
    """Generate embeddings for each line in a JSONL file."""
    
    texts = []
    embeddings = []
    metadata = []
    with open(file_path, "r") as f:
        total_lines = sum(1 for _ in f)
        f.seek(0)  


        for line in tqdm(f, total=total_lines, desc="Processing lines"):
            data = json.loads(line)
            text = data.get("text", "")
            texts.append(text)
            metadata_item = data.get("metadata", {})
            embedding = embed_text(text)
            embeddings.append(embedding)
            metadata.append(metadata_item)
    return texts, embeddings, metadata

def create_faiss_index(texts, embeddings, metadata, index_path: str):
    """Create and save a FAISS index from embeddings and metadata."""
    text_embeddings = list(zip(texts, embeddings))
    vector_store = FAISS.from_embeddings(text_embeddings, embedding=embedding_model, metadatas=metadata)
    vector_store.save_local(index_path)



if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Build FAISS index from JSONL file.")
    argparser.add_argument("--input_file", "-f", type=str, required=False, help="Path to the input JSONL file.")
    argparser.add_argument("--index_path", "-o", type=str, required=True, help="Path to save the FAISS index.")
    argparser.add_argument("--test", "-t", action='store_true', help="Test argument.")
    argparser.add_argument("--search", "-s", type=str, required=False, help="Search query.")
    args = argparser.parse_args()
    index_path = args.index_path
    if not args.test:
        jsonl_file_path = args.input_file
        texts, embeddings, metadata = embed_jsonl_file(jsonl_file_path)
        create_faiss_index(texts, embeddings, metadata, index_path)
    else:
        print("Test argument provided, skipping index creation.")
        load_store = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True) # safe because this FAISS index was created locally by us.
        print("Results: ", load_store.similarity_search(args.search, k=3))