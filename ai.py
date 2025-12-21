from dotenv import load_dotenv
from typing import Optional, List, Dict
import json
import os
from groq import Groq

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def dict_to_string(obj, level=0):
    """Convert dictionary to readable string format"""
    strings = []
    indent = "  " * level
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")
    return ", ".join(strings)


def retrieve_relevant_context(question: str, profile_id: int, limit: int = 5) -> Dict:
    """
    RAG STEP 1: RETRIEVAL
    Retrieve relevant financial notes using vector search
    
    Returns:
        Dict with:
        - retrieved_docs: List of relevant documents
        - similarity_scores: Relevance scores
        - retrieval_method: Method used (vector/keyword)
    """
    # Import from 'profiles.py' to avoid circular imports
    from profiles import search_notes_semantic
    
    try:
        # Perform semantic vector search
        results = search_notes_semantic(question, profile_id, limit=limit)
        
        # Check if fallback occurred (mock similarity score)
        retrieval_method = "vector_search"
        if results and results[0].get("$similarity") == 0.5:
            retrieval_method = "keyword_fallback"
        elif not results:
             retrieval_method = "none"

        if results:
            return {
                "retrieved_docs": [
                    {
                        "text": doc.get("text", ""),
                        "similarity_score": doc.get("$similarity", 0.0),
                        "metadata": doc.get("metadata", {})
                    }
                    for doc in results
                ],
                "retrieval_method": retrieval_method,
                "num_retrieved": len(results)
            }
        else:
            return {
                "retrieved_docs": [],
                "retrieval_method": "none",
                "num_retrieved": 0
            }
    except Exception as e:
        print(f"Retrieval error: {e}")
        return {
            "retrieved_docs": [],
            "retrieval_method": "error",
            "num_retrieved": 0,
            "error": str(e)
        }


def augment_prompt_with_context(question: str, profile: dict, retrieved_context: Dict) -> str:
    """
    RAG STEP 2: AUGMENTATION
    Combine user question with retrieved context and profile
    """
    profile_str = dict_to_string(profile)
    
    # Build context from retrieved documents
    context_sections = []
    if retrieved_context["retrieved_docs"]:
        context_sections.append("RELEVANT FINANCIAL NOTES (Retrieved from Vector Database):")
        for i, doc in enumerate(retrieved_context["retrieved_docs"], 1):
            similarity = doc.get("similarity_score", 0)
            text = doc.get("text", "")
            context_sections.append(f"{i}. [Relevance: {similarity:.2f}] {text}")
    else:
        context_sections.append("No relevant notes found in database.")
    
    context_str = "\n".join(context_sections)
    
    augmented_prompt = f"""You are a professional financial advisor with access to the user's financial profile and historical notes.

USER'S FINANCIAL PROFILE:
{profile_str}

{context_str}

USER'S QUESTION:
{question}

INSTRUCTIONS:
1. Use BOTH the profile data AND the retrieved notes to provide comprehensive advice
2. Reference specific notes when relevant (e.g., "Based on your note about...")
3. Provide specific, actionable recommendations
4. Format with proper spacing and clear structure
5. Use dollar amounts without decimals (e.g., $500 not $500.00)
6. DO NOT use LaTeX formatting or math syntax. Do not use dollar signs for LaTeX (e.g. no $x$).
7. If no relevant notes exist, rely on profile data only

Provide your financial advice:"""
    
    return augmented_prompt


def generate_rag_response(augmented_prompt: str) -> str:
    """
    RAG STEP 3: GENERATION
    Generate response using LLM with augmented context
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional financial advisor. Provide clear, well-formatted advice. Do not use LaTeX formatting."
                },
                {
                    "role": "user",
                    "content": augmented_prompt
                }
            ],
            temperature=0.2,
            max_tokens=800,
            top_p=0.9
        )
        
        text = response.choices[0].message.content
        
        # Post-process for better formatting
        import re
        
        # 1. Add space between number and text if missing (e.g., $100Monthly -> $100 Monthly)
        text = re.sub(r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)([a-zA-Z])', r'$\1 \2', text)
        
        # 2. Add spaces around math operators
        text = re.sub(r'(\d)([-+*/])(\d)', r'\1 \2 \3', text)
        
        # 3. Fix concatenated words
        text = re.sub(r'permonth', 'per month', text)
        text = re.sub(r'peryear', 'per year', text)
        
        # 4. Remove .00 decimals
        text = re.sub(r'\$(\d+(?:,\d{3})*)\.00\b', r'$\1', text)

        # 5. CRITICAL FIX FOR FONT ISSUE:
        # Streamlit interprets $...$ as LaTeX math mode, which changes the font.
        # We replace all literal $ with \$ to escape them.
        text = text.replace('$', '\\$')
        
        return text
        
    except Exception as e:
        return f"Error generating response: {str(e)}"


def ask_ai_with_rag(profile: dict, question: str, profile_id: int) -> Dict:
    """
    COMPLETE RAG PIPELINE
    """
    # Step 1: RETRIEVAL
    print(f"[RAG] Step 1: Retrieving relevant context for: '{question}'")
    retrieved_context = retrieve_relevant_context(question, profile_id, limit=5)
    print(f"[RAG] Retrieved {retrieved_context['num_retrieved']} documents using {retrieved_context['retrieval_method']}")
    
    # Step 2: AUGMENTATION
    print(f"[RAG] Step 2: Augmenting prompt with retrieved context")
    augmented_prompt = augment_prompt_with_context(question, profile, retrieved_context)
    
    # Step 3: GENERATION
    print(f"[RAG] Step 3: Generating response with LLM")
    response = generate_rag_response(augmented_prompt)
    
    # Return full pipeline information
    return {
        "response": response,
        "rag_pipeline": {
            "retrieval": {
                "method": retrieved_context["retrieval_method"],
                "num_documents": retrieved_context["num_retrieved"],
                "documents": retrieved_context["retrieved_docs"]
            },
            "augmentation": {
                "context_length": len(augmented_prompt),
                "has_context": len(retrieved_context["retrieved_docs"]) > 0
            },
            "generation": {
                "model": "llama-3.3-70b-versatile",
                "temperature": 0.2
            }
        }
    }


def get_budget(profile, goals):
    """
    Uses Groq to calculate optimal budget allocation
    """
    try:
        profile_str = dict_to_string(profile)
        goals_str = ", ".join(goals) if isinstance(goals, list) else str(goals)
        
        monthly_income = profile.get("monthly_income", 5000)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are a financial planning expert calculating optimal budget allocation.

USER'S PROFILE:
{profile_str}

FINANCIAL GOALS:
{goals_str}

RULES FOR BUDGET CALCULATION:
1. All category amounts MUST add up to exactly the monthly_income: ${monthly_income}
2. Use the 50/30/20 rule as baseline: 50% needs, 30% wants, 20% savings
3. Adjust based on debt and goals
4. Housing should be 25-35% of income
5. Food should be 10-15% of income
6. Transportation should be 10-15% of income
7. Savings should be at least 15-20% of income (more if building emergency fund)
8. Entertainment should be 5-10% of income
9. Miscellaneous should be 5-10% of income

CRITICAL: Return ONLY valid JSON with NO additional text, explanations, or markdown formatting.

Return format (replace with calculated numbers, MUST sum to ${monthly_income}):
{{"housing": 1500, "food": 500, "transportation": 300, "savings": 1000, "entertainment": 200, "miscellaneous": 500}}"""
                }
            ],
            temperature=0.2,
            max_tokens=500
        )
        
        # Extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', response.choices[0].message.content, re.DOTALL)
        if json_match:
            budget = json.loads(json_match.group())
            
            # Verify the budget adds up correctly
            total = sum(budget.values())
            if abs(total - monthly_income) > 10:
                print(f"⚠️ Warning: Budget doesn't add up. Total: ${total}, Income: ${monthly_income}")
            
            return budget
        else:
            # Fallback default values
            income = profile.get("monthly_income", 5000)
            return {
                "housing": int(income * 0.30),
                "food": int(income * 0.12),
                "transportation": int(income * 0.10),
                "savings": int(income * 0.20),
                "entertainment": int(income * 0.08),
                "miscellaneous": int(income * 0.20)
            }
            
    except Exception as e:
        print(f"Error getting budget: {e}")
        income = profile.get("monthly_income", 5000)
        return {
            "housing": int(income * 0.30),
            "food": int(income * 0.12),
            "transportation": int(income * 0.10),
            "savings": int(income * 0.20),
            "entertainment": int(income * 0.08),
            "miscellaneous": int(income * 0.20)
        }
