import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHROMA_PERSIST_DIRECTORY = "chroma_db"
CHROMA_COLLECTION_NAME = "bug-reports"

MODEL = "gpt-4o-mini"
MAX_TOKENS = 4000
