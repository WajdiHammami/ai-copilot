"""Centralized configuration for Azure OpenAI and paths."""
import os
from typing import Optional
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.utilities import SQLDatabase
import dotenv

dotenv.load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

AZURE_EMBEDDINGS_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT_EMBEDDINGS")
AZURE_EMBEDDINGS_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME")
AZURE_EMBEDDINGS_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION_EMBEDDINGS")
AZURE_EMBEDDINGS_API_KEY = os.getenv("AZURE_OPENAI_API_KEY_EMBEDDINGS")

# Paths
DEFAULT_FAISS_INDEX_PATH = "data/embeddings/faiss-index/"
DEFAULT_LOG_DIR = "logs"

# ===== Client Factories =====
_llm_instance: Optional[AzureChatOpenAI] = None
_embedding_instance: Optional[AzureOpenAIEmbeddings] = None


def get_llm(temperature: float = 0) -> AzureChatOpenAI:
    """Get or create the Azure Chat LLM instance (singleton)."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            deployment_name=AZURE_OPENAI_DEPLOYMENT,
            api_version=AZURE_OPENAI_API_VERSION,
            api_key=AZURE_OPENAI_API_KEY,
            temperature=temperature,
        )
    return _llm_instance


def get_embedding_model() -> AzureOpenAIEmbeddings:
    """Get or create the Azure Embeddings instance (singleton)."""
    global _embedding_instance
    if _embedding_instance is None:
        _embedding_instance = AzureOpenAIEmbeddings(
            azure_endpoint=AZURE_EMBEDDINGS_ENDPOINT,
            azure_deployment=AZURE_EMBEDDINGS_DEPLOYMENT,
            api_version=AZURE_EMBEDDINGS_API_VERSION,
            api_key=AZURE_EMBEDDINGS_API_KEY,
        )
    return _embedding_instance


def load_vector_store(index_path: str = DEFAULT_FAISS_INDEX_PATH) -> FAISS:
    """Load FAISS vector store from disk."""
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found at: {index_path}")
    
    embeddings = get_embedding_model()
    return FAISS.load_local(
        index_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True  # Only for trusted local indexes.
    )