from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

ENDPOINT = os.getenv("ASTRA_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")


@st.cache_resource
def get_db():
    client = DataAPIClient(TOKEN)
    db = client.get_database_by_api_endpoint(ENDPOINT)
    return db

def ensure_collections():
    """Ensure both collections exist with proper configuration"""
    db = get_db()
    
    # Get list of existing collections
    existing_collections = db.list_collection_names()
    
    # Create financial_profiles if it doesn't exist
    if "financial_profiles" not in existing_collections:
        try:
            db.create_collection("financial_profiles")
            print("✓ Created collection: financial_profiles")
        except Exception as e:
            print(f"Error creating financial_profiles: {e}")
    else:
        print("✓ Collection financial_profiles exists")
    
    # Create financial_notes with vector support if it doesn't exist
    if "financial_notes" not in existing_collections:
        try:
            # Try with vector configuration
            db.create_collection(
                "financial_notes",
                dimension=1024,
                metric="cosine",
                service={
                    "provider": "nvidia",
                    "modelName": "NV-Embed-QA"
                }
            )
            print("✓ Created collection: financial_notes (with vector embeddings)")
        except Exception as e:
            print(f"⚠️  Error creating financial_notes with vectors: {e}")
            print("   Trying without vector configuration...")
            try:
                # Fallback: create without vectors
                db.create_collection("financial_notes")
                print("✓ Created collection: financial_notes (without vectors)")
                print("   Note: Vector search will not be available")
            except Exception as e2:
                print(f"❌ Failed to create financial_notes: {e2}")
    else:
        print("✓ Collection financial_notes exists")

# Initialize database and ensure collections exist
db = get_db()
ensure_collections()

# Get collection references
personal_data_collection = db.get_collection("financial_profiles")
notes_collection = db.get_collection("financial_notes")

print("✓ Connected to AstraDB for Financial Advisor")
print(f"  - Profiles: financial_profiles")
print(f"  - Notes: financial_notes")