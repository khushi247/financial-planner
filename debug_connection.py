import os
from dotenv import load_dotenv

load_dotenv()

print("=== Checking Your Astra DB Configuration ===")
print("ASTRA_DB_APPLICATION_TOKEN:", os.getenv("ASTRA_DB_APPLICATION_TOKEN")[:20] + "..." if os.getenv("ASTRA_DB_APPLICATION_TOKEN") else "MISSING")
print("ASTRA_DB_ID:", os.getenv("ASTRA_DB_ID"))
print("ASTRA_DB_REGION:", os.getenv("ASTRA_DB_REGION"))
print("ASTRA_DB_KEYSPACE:", os.getenv("ASTRA_DB_KEYSPACE"))

# Build the URL that's failing
db_id = os.getenv("ASTRA_DB_ID")
region = os.getenv("ASTRA_DB_REGION")
if db_id and region:
    url = f"https://{db_id}-{region}.apps.astra.datastax.com"
    print("\n=== Connection URL Being Generated ===")
    print("URL:", url)
    print("\nThis URL should match what's in your Astra DB dashboard!")
else:
    print("\n❌ Missing ASTRA_DB_ID or ASTRA_DB_REGION in .env file!")