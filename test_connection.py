import os
from dotenv import load_dotenv
from astrapy import DataAPIClient

load_dotenv()

print("Testing Astra DB connection...")
print("Token starts with:", os.getenv("ASTRA_DB_APPLICATION_TOKEN")[:20] + "...")

try:
    client = DataAPIClient(os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
    db = client.get_database_by_api_endpoint(
        f"https://{os.getenv('ASTRA_DB_ID')}-{os.getenv('ASTRA_DB_REGION')}.apps.astra.datastax.com"
    )
    
    print("✅ Connected to Astra DB successfully!")
    print("Collecti" \
    "ons found:", db.list_collection_names())
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("Please check:")
    print("1. Is your token correct? (starts with 'AstraCS:')")
    print("2. Is your database ID correct?")
    print("3. Is your region correct?")
    print("4. Is your database status 'Active'?")