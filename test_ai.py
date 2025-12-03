"""
Test script to verify AI responses are properly formatted
Run this to check AI output before using in the app
"""

from ai import ask_ai
from dotenv import load_dotenv

load_dotenv()

# Sample profile for testing
test_profile = {
    "general": {
        "name": "Test User",
        "age": 35,
        "monthly_income": 10000,
        "current_savings": 20000,
        "employment_status": "Full-time",
        "debt_amount": 0,
        "dependents": 2
    },
    "goals": ["Build Emergency Fund", "Investment Growth"],
    "budget": {
        "monthly_income": 10000,
        "housing": 2500,
        "food": 1200,
        "transportation": 500,
        "savings": 2000,
        "entertainment": 800,
        "miscellaneous": 1000
    }
}

# Test questions
questions = [
    "Which area can I cut from to invest more without compromising my lifestyle?",
    "How much should I save for emergencies?",
    "What percentage of income should go to housing?"
]

print("=" * 80)
print("TESTING AI RESPONSES FOR FORMATTING")
print("=" * 80)

for i, question in enumerate(questions, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST {i}: {question}")
    print(f"{'=' * 80}\n")
    
    response = ask_ai(test_profile, question)
    print(response)
    
    # Check for formatting issues
    print("\n" + "-" * 80)
    print("FORMATTING CHECK:")
    
    issues = []
    
    # Check for concatenated text
    if "permonth" in response.lower():
        issues.append("❌ Found 'permonth' - should be 'per month'")
    if "peryear" in response.lower():
        issues.append("❌ Found 'peryear' - should be 'per year'")
    
    # Check for dollar sign spacing
    import re
    bad_dollars = re.findall(r'\$\d+[a-zA-Z]', response)
    if bad_dollars:
        issues.append(f"❌ Found dollar amounts without spaces: {bad_dollars}")
    
    # Check for .00 decimals
    if ".00" in response:
        issues.append("⚠️  Found .00 decimals (should be removed for cleaner look)")
    
    if not issues:
        print("✅ No formatting issues detected!")
    else:
        for issue in issues:
            print(issue)
    
    print("-" * 80)

print("\n" + "=" * 80)
print("TESTING COMPLETE")
print("=" * 80)