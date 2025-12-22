💰 Personal Finance & Budget Advisor
AI-Powered Personal Finance Management Application
An intelligent personal finance assistant that helps users track income and expenses, set financial goals, and receive AI-driven budgeting and financial advice.
Built with Streamlit, Groq (Llama 3.3 70B), AstraDB, and optional Langflow workflows.

🎯 Overview
This application transforms personal financial management by providing:


🤖 Budget Allocation AI – Automatically generates optimized monthly budgets


💬 Financial Question Answering – Ask personalized finance questions and get expert AI advice


🎯 Goal Tracking – Monitor progress toward savings, debt payoff, retirement, and more


📝 Financial Notes – Store important financial information with vector search


🔀 Smart Routing – Automatically detects when calculations are required vs. general advice



🏗️ Architecture
Core Components
Streamlit Frontend (main.py)


Personal financial data input forms


AI-powered budget allocation interface


Financial advisor chat


Financial notes management


AI Backend (ai.py)


Uses Groq’s free LLM API (Llama 3.3 70B)


ask_ai() – General financial advice


get_budget() – Intelligent budget allocation


Database Layer (db.py, profiles.py)


AstraDB for persistence


Stores user profiles and financial notes


Vector search for relevant note retrieval


Langflow Workflows (/flows)


AskFinancialAdvisorV2 – Conditional routing between calculations and advice


Budget Allocation Flow – AI-powered budget generation



📊 Data Structure
User Profile Schema
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


AstraDB account (free tier)


Groq API key (free)


OpenAI API key (optional – required only for Langflow)



Installation
1️⃣ Clone the repository
git clone <your-repo-url>
cd personal-finance-advisor

2️⃣ Install dependencies
pip install streamlit astrapy groq python-dotenv


3️⃣ Create a NEW AstraDB Database


Go to 👉 https://astra.datastax.com


Click Create Database


Database name: financial_advisor


Keyspace: finance_data


Provider: AWS / GCP / Azure


Region: Choose the closest region


Click Create Database and wait until status is Active


Click Generate Token and save it



4️⃣ Configure Environment Variables
Create a .env file in the project root:
# AstraDB Configuration
ASTRA_DB_APPLICATION_TOKEN=AstraCS:...
ASTRA_DB_ID=your-new-db-id
ASTRA_DB_REGION=us-east1
ASTRA_DB_KEYSPACE=finance_data
ASTRA_ENDPOINT=https://your-db-id-your-region.apps.astra.datastax.com

# API Keys
GROQ_API_KEY=gsk_...
OPENAI_API_KEY=sk-...   # Optional (Langflow only)


5️⃣ Test Database Connection
python test_connection.py


6️⃣ Run the Application
streamlit run main.py


📁 Project Structure
financial-advisor/
├── main.py                  # Streamlit app entry point
├── ai.py                    # AI logic (Groq integration)
├── db.py                    # Database connection
├── profiles.py              # Profile CRUD operations
├── form_submit.py           # Form handlers
├── test_connection.py       # DB connection tester
├── debug_connection.py      # DB debugging tool
├── prompts/
│   ├── conditional_router.txt
│   ├── general_agent.txt
│   ├── budget.txt
│   └── tool_calling_agent.txt
└── flows/
    ├── AskAIV2.json
    └── Budget Flow.json


🎨 Features
1️⃣ Personal Financial Dashboard


Track income, savings, debt, and dependents


Employment status tracking


Age-based financial recommendations



2️⃣ Financial Goals
Choose from:


🏦 Build Emergency Fund


💳 Pay Off Debt


🏖️ Save for Retirement


🏠 Buy a Home


📈 Investment Growth



3️⃣ AI-Powered Budget Allocation
Click “Generate with AI” to receive a personalized budget:


Housing (rent/mortgage)


Food & groceries


Transportation


Savings targets


Entertainment


Miscellaneous expenses



4️⃣ Intelligent Financial Advisor
Ask questions like:


“How much should I save each month?”


“What’s the best way to pay off my debt?”


“How can I build an emergency fund with my income?”



5️⃣ Financial Notes with Vector Search


Store important financial information


AI-powered semantic search


Notes automatically retrieved during related questions



🔄 Langflow Integration
AskFinancialAdvisorV2 Flow


User asks a financial question


Conditional router determines if calculation is needed


YES → Calculator tool + agent


NO → General financial advisor prompt


User profile + notes are always available



Budget Allocation Flow


Takes user profile + financial goals


Uses optimized prompt template


Generates structured JSON budget output



🛠️ Customization
Add New Financial Goals
Edit main.py:
goals = st.multiselect(
    "Select your Financial Goals",
    ["Build Emergency Fund", "Your New Goal"],
)


Modify Budget Categories
Edit profiles.py:
"budget": {
    "monthly_income": 5000,
    "housing": 1500,
    "your_new_category": 300,
}


Change AI Model
Edit ai.py:
model="llama-3.3-70b-versatile"


🧪 Testing
Test Database Connection
python test_connection.py

Debug Configuration
python debug_connection.py

Test AI Functions
from ai import ask_ai

profile = {"general": {"monthly_income": 5000}}
result = ask_ai(profile, "How much should I save?")
print(result)


📈 Use Cases


Personal budgeting & expense optimization


Debt management strategies


Savings & retirement planning


Financial education via AI


Expense and recurring bill tracking



🔐 Security Notes


Never commit .env files


Rotate AstraDB tokens regularly


Use Streamlit Secrets for production deployments



🚦 Roadmap


Expense tracking


Investment portfolio analysis


Bill reminders


Multi-currency support


Financial report exports


Mobile app version



📝 License
MIT License – free for personal and commercial use.

🤝 Contributing
Contributions are welcome!
Please open an issue or submit a pull request.


Built with ❤️ using Streamlit, Groq, and AstraDB
