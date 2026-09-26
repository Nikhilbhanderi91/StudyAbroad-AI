import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
MASTER_DATASET_DIR = BASE_DIR / "Master Dataset"
OUTPUT_DIR = BASE_DIR / "Output"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
PROMPTS_DIR = BASE_DIR / "prompts"

# Ensure directories exist
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Embedding Configuration
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = 384  # for all-MiniLM-L6-v2

# FAISS Configuration
FAISS_INDEX_PATH = VECTOR_STORE_DIR / "studyabroad_faiss.index"
FAISS_METADATA_PATH = VECTOR_STORE_DIR / "studyabroad_metadata.json"
DOCUMENTS_CORPUS_PATH = KNOWLEDGE_BASE_DIR / "studyabroad_corpus.json"

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")

# Currency Conversion Constants (to INR)
EXCHANGE_RATES = {
    "USD": 83.5,
    "GBP": 106.0,
    "EUR": 90.5,
    "AUD": 54.5,
    "CAD": 61.5,
    "SGD": 62.0,
    "INR": 1.0
}
