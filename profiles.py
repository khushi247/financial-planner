from db import personal_data_collection, notes_collection
# 're' is no longer needed as the regex fallback is not supported
# import re 

def get_values(id):
    return {
        "id": id, 
        "general": {
            "name": "",
            "age": 30,
            "monthly_income": 5000,
            "current_savings": 10000,
            "employment_status": "Full-time",
            "debt_amount": 0,
            "dependents": 0
        },
        "goals": ["Build Emergency Fund"],
        "budget": {
            "housing": 1500,
            "food": 500,
            "transportation": 300,
            "savings": 1000,
            "entertainment": 200,
            "miscellaneous": 500
        },
    }
    
def create_profile(id):
    # This function is the one main.py is trying to import
    profile_values = get_values(id)
    result = personal_data_collection.insert_one(profile_values)
    return id, profile_values

def get_profile(id):
    return personal_data_collection.find_one({"id": {"$eq": id}})

def get_notes(profile_id: int):
    """Get all notes for a user (for display purposes, not RAG)"""
    try:
        # FIXED: Changed .sort("metadata.injested", -1) to .sort({"metadata.injested": -1})
        return list(notes_collection.find({"user_id": profile_id}).sort({"metadata.injested": -1}))
    except Exception as e:
        print(f"Error fetching notes: {e}")
        return []

def search_notes_semantic(query: str, profile_id: int, limit: int = 5):
    """
    RAG RETRIEVAL FUNCTION
    
    Search financial notes using semantic similarity (vector search)
    """
    try:
        print(f"[RAG RETRIEVAL] Searching for: '{query}'")
        print(f"[RAG RETRIEVAL] Method: Vector semantic search")
        
        # FIXED: Using sort={"$vectorize": query} for DataAPIClient
        results = list(notes_collection.find(
            filter={"user_id": profile_id},  # The filter for the user
            sort={"$vectorize": query},      # The query string to vectorize and search for
            limit=limit,
            include_similarity=True         # Get similarity scores
        ))
        
        print(f"[RAG RETRIEVAL] Found {len(results)} relevant documents")
        
        for i, doc in enumerate(results, 1):
            score = doc.get("$similarity", 0)
            text_preview = doc.get("text", "")[:50]
            print(f"[RAG RETRIEVAL] Doc {i}: Similarity={score:.3f}, Text='{text_preview}...'")
        
        return results
        
    except Exception as e:
        print(f"[RAG RETRIEVAL] Error with vector search: {e}")
        print(f"[RAG RETRIEVAL] Vector search failed. No fallback available for Data API.")
        return []