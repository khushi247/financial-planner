# from db import personal_data_collection, notes_collection
# from datetime import datetime, timezone

# def update_personal_info(existing, update_type, **kwargs):
#     if update_type == "goals":
#         existing["goals"] = kwargs.get("goals", [])
#         update_field = {"goals": existing["goals"]}
#     else:
#         existing[update_type] = kwargs
#         update_field = {update_type: existing[update_type]}
 
#     personal_data_collection.update_one(
#         {"id": existing["id"]}, {"$set": update_field}
#     )
#     return existing

# def add_note(note, profile_id):
#     """
#     Add financial note with vector embeddings for RAG retrieval
    
#     This is a critical part of the RAG system:
#     - Stores the note text
#     - Automatically creates vector embedding via $vectorize
#     - Enables semantic search for retrieval
#     """
#     new_note = {
#         "user_id": profile_id,
#         "text": note,
#         "metadata": {
#             "injested": datetime.now(timezone.utc),
#             "note_type": "financial",
#             "indexed_for_rag": True  # Flag for RAG system
#         },
#     }
    
#     # Try to add vector embeddings for RAG, but don't fail if not supported
#     try:
#         new_note["$vectorize"] = note  # Enable vector embeddings for semantic search
#         print(f"[RAG] Note added with vector embeddings: '{note[:50]}...'")
#     except Exception as e:
#         print(f"[RAG] Warning: Vector embeddings not available: {e}")
#         pass
    
#     result = notes_collection.insert_one(new_note)
#     new_note["_id"] = result.inserted_id
#     return new_note

# def delete_note(id):
#     """Delete a note from the vector database"""
#     result = notes_collection.delete_one({"_id": id})
#     print(f"[RAG] Note deleted from vector DB")
#     return result

# def search_notes_semantic(query: str, profile_id: int, limit: int = 5):
#     """
#     RAG RETRIEVAL FUNCTION
    
#     Search financial notes using semantic similarity (vector search)
#     This is the core retrieval mechanism for RAG
    
#     Args:
#         query: User's question (will be embedded and compared)
#         profile_id: User ID to filter notes
#         limit: Number of documents to retrieve
    
#     Returns:
#         List of documents with similarity scores
    
#     Example:
#         query = "how to save money on groceries"
#         Will find notes about:
#         - "meal planning tips"
#         - "buy generic brands"
#         - "use coupons weekly"
#         Even if exact words don't match!
#     """
#     try:
#         print(f"[RAG RETRIEVAL] Searching for: '{query}'")
#         print(f"[RAG RETRIEVAL] Method: Vector semantic search")
        
#         # Vector search using $vectorize - this is true RAG retrieval!
#         results = list(notes_collection.find(
#             {
#                 "user_id": profile_id,
#                 "$vectorize": query  # Astra automatically embeds query and finds similar vectors
#             },
#             limit=limit,
#             include_similarity=True  # Get similarity scores
#         ))
        
#         print(f"[RAG RETRIEVAL] Found {len(results)} relevant documents")
        
#         # Log similarity scores for transparency
#         for i, doc in enumerate(results, 1):
#             score = doc.get("$similarity", 0)
#             text_preview = doc.get("text", "")[:50]
#             print(f"[RAG RETRIEVAL] Doc {i}: Similarity={score:.3f}, Text='{text_preview}...'")
        
#         return results
        
#     except Exception as e:
#         print(f"[RAG RETRIEVAL] Error with vector search: {e}")
#         print(f"[RAG RETRIEVAL] Falling back to keyword search")
        
#         # Fallback to keyword search if vectors not available
#         try:
#             import re
#             # Simple keyword-based search as fallback
#             results = list(notes_collection.find(
#                 {
#                     "user_id": profile_id,
#                     "text": {"$regex": re.escape(query), "$options": "i"}
#                 },
#                 limit=limit
#             ))
            
#             # Add mock similarity scores for consistency
#             for doc in results:
#                 doc["$similarity"] = 0.5  # Mock score
            
#             print(f"[RAG RETRIEVAL] Fallback found {len(results)} documents")
#             return results
            
#         except Exception as e2:
#             print(f"[RAG RETRIEVAL] Fallback search also failed: {e2}")
#             return []

# def get_all_notes(profile_id: int):
#     """Get all notes for a user (for display purposes, not RAG)"""
#     try:
#         return list(notes_collection.find({"user_id": profile_id}).sort("metadata.injested", -1))
#     except Exception as e:
#         print(f"Error fetching notes: {e}")
#         return []


from db import personal_data_collection, notes_collection
from datetime import datetime, timezone
# 're' import removed as it's no longer needed here

def update_personal_info(existing, update_type, **kwargs):
    if update_type == "goals":
        existing["goals"] = kwargs.get("goals", [])
        update_field = {"goals": existing["goals"]}
    else:
        # This will correctly handle saving the 'budget' dict
        existing[update_type] = kwargs
        update_field = {update_type: existing[update_type]}
 
    personal_data_collection.update_one(
        {"id": existing["id"]}, {"$set": update_field}
    )
    return existing

def add_note(note, profile_id):
    """
    Add financial note with vector embeddings for RAG retrieval
    
    This is a critical part of the RAG system:
    - Stores the note text
    - Automatically creates vector embedding via $vectorize
    - Enables semantic search for retrieval
    """
    new_note = {
        "user_id": profile_id,
        "text": note,
        "metadata": {
            "injested": datetime.now(timezone.utc),
            "note_type": "financial",
            "indexed_for_rag": True  # Flag for RAG system
        },
    }
    
    # Try to add vector embeddings for RAG, but don't fail if not supported
    try:
        new_note["$vectorize"] = note  # Enable vector embeddings for semantic search
        print(f"[RAG] Note added with vector embeddings: '{note[:50]}...'")
    except Exception as e:
        print(f"[RAG] Warning: Vector embeddings not available: {e}")
        pass
    
    result = notes_collection.insert_one(new_note)
    new_note["_id"] = result.inserted_id
    return new_note

def delete_note(id):
    """Delete a note from the vector database"""
    result = notes_collection.delete_one({"_id": id})
    print(f"[RAG] Note deleted from vector DB")
    return result

# --- REMOVED: search_notes_semantic ---
# --- REMOVED: get_all_notes ---