Personal Finance & Budget Advisor 💰
An AI-powered personal finance management application that helps users track their income, expenses, and financial goals while providing intelligent budgeting recommendations.

🎯 Overview
This application transforms personal financial management by providing:

Budget Allocation AI: Automatically generates optimal budget breakdowns
Financial Question Answering: Get expert financial advice powered by AI
Goal Tracking: Set and monitor financial goals (emergency fund, debt payoff, retirement, etc.)
Financial Notes: Store important financial information with vector search capabilities
Smart Routing: Automatically detects if calculations are needed vs. general advice
🏗️ Architecture
Key Components
Streamlit Frontend (main.py)
Personal financial data input forms
Budget allocation interface
AI-powered financial advisor chat
Financial notes management
AI Backend (ai.py)
Uses Groq's free LLM API (Llama 3.3 70B)
ask_ai(): General financial advice
get_budget(): Intelligent budget allocation
Database Layer (db.py, profiles.py)
AstraDB for data persistence
Stores user profiles and financial notes
Vector search for relevant note retrieval
Langflow Workflows (JSON files)
AskFinancialAdvisorV2: Conditional routing between calculations and advice
Budget Allocation Flow: AI-powered budget generation
📊 Data Structure
User Profile
python
{
    "id": 1,
    "general": {
        "name": str,
        "age": int,
        "monthly_income": float,
        "current_savings": float,
        "employment_status": str,  # Full-time, Part-time, Self-employed, etc.
        "debt_amount": float,
        "dependents": int
    },
    "goals": [str],  # ["Build Emergency Fund", "Pay Off Debt", ...]
    "budget": {
        "monthly_income": int,
        "housing": int,
        "food": int,
        "transportation": int,
        "savings": int,
        "entertainment": int,
        "miscellaneous": int
    }
}
🚀 Setup Instructions
Prerequisites
Python 3.8+
AstraDB account (free tier available)
Groq API key (free)
OpenAI API key (for Langflow - optional)
Installation
Clone the repository
bash
git clone <your-repo>
cd personal-finance-advisor
Install dependencies
bash
pip install streamlit astrapy groq python-dotenv
Create a NEW AstraDB Database
Go to https://astra.datastax.com
Click "Create Database"
Database name: financial_advisor
Keyspace: finance_data
Provider: AWS/GCP/Azure (your choice)
Region: Choose closest to you
Click "Create Database"
Wait for status to become "Active"
Click "Generate Token" and save it
Configure environment variables Create a .env file:
env
# AstraDB Configuration - NEW DATABASE
ASTRA_DB_APPLICATION_TOKEN=AstraCS:...  # Your NEW token
ASTRA_DB_ID=your-new-db-id             # From new database
ASTRA_DB_REGION=us-east1                # Your chosen region
ASTRA_DB_KEYSPACE=finance_data          # New keyspace name
ASTRA_ENDPOINT=https://your-new-db-id-your-region.apps.astra.datastax.com

# API Keys
GROQ_API_KEY=gsk_...
OPENAI_API_KEY=sk-...  # Optional, for Langflow
Test database connection
bash
python test_connection.py
Run the application
bash
streamlit run main.py
📁 Project Structure
financial-advisor/
├── main.py                 # Streamlit app entry point
├── ai.py                   # AI logic (Groq integration)
├── db.py                   # Database connection
├── profiles.py             # Profile CRUD operations
├── form_submit.py          # Form handlers
├── test_connection.py      # DB connection tester
├── debug_connection.py     # DB debugging tool
├── prompts/
│   ├── conditional_router.txt
│   ├── general_agent.txt
│   ├── budget.txt
│   └── tool_calling_agent.txt
└── flows/
    ├── AskAIV2.json
    └── Budget Flow.json
🎨 Features
1. Personal Financial Dashboard
Track income, savings, debt, and dependents
Monitor employment status
Age-based financial recommendations
2. Financial Goals
Choose from:

🏦 Build Emergency Fund
💳 Pay Off Debt
🏖️ Save for Retirement
🏠 Buy a Home
📈 Investment Growth
3. AI-Powered Budget Allocation
Click "Generate with AI" to get personalized budget recommendations:

Housing (rent/mortgage)
Food & groceries
Transportation
Savings targets
Entertainment allowance
Miscellaneous expenses
4. Intelligent Financial Advisor
Ask questions like:

"How much should I save each month?"
"What's the best way to pay off my debt?"
"How can I build an emergency fund with my income?"
5. Financial Notes with Vector Search
Store important financial information
AI-powered semantic search
Automatically retrieved when asking related questions
🔄 Langflow Integration
AskFinancialAdvisorV2 Flow
User asks a financial question
Conditional router determines if calculation is needed
If YES: Uses calculator tool + agent for numerical answers
If NO: Uses general financial advisor prompt
Both paths have access to user profile and stored notes
Budget Allocation Flow
Takes user profile + financial goals as input
Feeds into optimized prompt template
OpenAI generates JSON budget allocation
Returns structured budget breakdown
🛠️ Customization
Adding New Financial Goals
Edit main.py:

python
goals = st.multiselect(
    "Select your Financial Goals",
    ["Build Emergency Fund", "Your New Goal", ...],
    ...
)
Modifying Budget Categories
Edit profiles.py default values:

python
"budget": {
    "monthly_income": 5000,
    "housing": 1500,
    "your_new_category": 300,  # Add here
    ...
}
Changing AI Model
Edit ai.py:

python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # Change model here
    ...
)
🧪 Testing
Test Database Connection
bash
python test_connection.py
Debug Configuration
bash
python debug_connection.py
Test AI Integration
python
from ai import ask_ai, get_budget

profile = {"general": {"monthly_income": 5000, ...}}
result = ask_ai(profile, "How much should I save?")
print(result)
📈 Use Cases
Personal Budgeting: Track and optimize monthly spending
Debt Management: Create strategies to pay off loans
Savings Goals: Plan for major purchases or retirement
Financial Education: Learn about personal finance through AI chat
Expense Tracking: Keep notes on recurring expenses
🔐 Security Notes
Never commit .env file to version control
Keep API keys secure
AstraDB tokens should be rotated regularly
Use Streamlit secrets for production deployment
🚦 Roadmap
 Add expense tracking features
 Investment portfolio analysis
 Bill reminder system
 Multi-currency support
 Export financial reports
 Mobile app version
📝 License
MIT License - feel free to use for personal or commercial projects

🤝 Contributing
Contributions welcome! Please open an issue or submit a PR.

💡 From Fitness to Finance
This project was originally a fitness tracking app and was transformed into a financial advisor by:

Replacing health metrics with financial metrics
Changing nutrition macros to budget allocation
Updating all AI prompts for financial context
Adapting goals from fitness to financial objectives
The core architecture remains the same, demonstrating how versatile the pattern is!

Built with ❤️ using Streamlit, Groq, and AstraDB

