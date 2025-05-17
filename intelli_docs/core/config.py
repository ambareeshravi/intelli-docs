from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load model.env file
load_dotenv('model.env')

class Settings(BaseSettings):
    """
    Contains all the settings to run the application
    """
    # Application settings
    APP_NAME: str = "Intelligent Document Q&A System"
    API_V1_STR: str = "/api/v1"
    
    # Document processing settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_DOCUMENT_SIZE: int = 24 * 1024 * 1024  # 24MB
    
    # Vector store settings
    VECTOR_STORE_PATH: Path = Path("data/processed/vector_store")
    
    # LLM settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = os.getenv('OLLAMA_MODEL', 'llama3.2:3b')  # Read from model.env
    
    # Embedding settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # File paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"

    # Ensure directories exist
    RAW_DATA_DIR.mkdir(exist_ok=True, parents=True)
    PROCESSED_DATA_DIR.mkdir(exist_ok=True, parents=True)
    VECTOR_STORE_PATH.mkdir(exist_ok=True, parents=True) 
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()
