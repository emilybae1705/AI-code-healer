import chromadb
from config import OPENAI_API_KEY, CHROMA_PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME


def test_chroma_setup():
    """Test ChromaDB setup and basic operations."""
    try:
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)

        # Create or get collection
        collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

        print("✅ ChromaDB setup successful!")
        print(f"Collection '{CHROMA_COLLECTION_NAME}' is ready.")

        return True
    except Exception as e:
        print(f"❌ Error setting up ChromaDB: {str(e)}")
        return False


def test_openai_setup():
    """Test OpenAI API key setup."""
    if not OPENAI_API_KEY:
        print("❌ OpenAI API key not found. Please set it in your .env file.")
        return False

    print("✅ OpenAI API key found!")
    return True


if __name__ == "__main__":
    print("Testing setup...")
    openai_ok = test_openai_setup()
    chroma_ok = test_chroma_setup()

    if openai_ok and chroma_ok:
        print("\n✨ All tests passed! You're ready to start building your AI agent.")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
