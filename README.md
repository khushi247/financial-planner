No, the text you pasted above is **not** formatted as valid Markdown code. It looks like "plain text" where the special formatting symbols (like `#` for headings or ````` for code blocks) are missing.

If you paste that directly into a `README.md` file on GitHub, it will look like a messy wall of text without any bolding, boxes, or links.

### How to fix it:

You need to copy the **raw source code** inside the box below. Do not copy the text that looks "pretty" or "rendered"—copy the text that has the hashtags (`#`) and backticks (`````).

Here is the correct raw Markdown code again. **Click the "Copy" button** in the top right corner of this code block:

```markdown
# 💰 Personal Finance & Budget Advisor

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![AstraDB](https://img.shields.io/badge/AstraDB-DataStax-purple)
![Groq](https://img.shields.io/badge/AI-Groq%20Llama3-orange)

An AI-powered personal finance management application that helps users track their income, expenses, and financial goals while providing intelligent budgeting recommendations.

---

## 🎯 Overview

This application transforms personal financial management by providing:

* **Budget Allocation AI:** Automatically generates optimal budget breakdowns based on your profile.
* **Financial Question Answering:** Get expert financial advice powered by Llama 3.3 (via Groq).
* **Goal Tracking:** Set and monitor financial goals (Emergency Fund, Debt Payoff, Retirement, etc.).
* **Financial Notes:** Store important financial information with vector search capabilities.
* **Smart Routing:** Automatically detects if specific calculations are needed or general advice is sufficient.

---

## 🏗️ Architecture

### Key Components
1.  **Streamlit Frontend (`main.py`):** Handles user input, dashboard visualization, and chat interfaces.
2.  **AI Backend (`ai.py`):** Integrates with Groq's free LLM API (Llama 3.3 70B) for advice and budgeting.
3.  **Database Layer (`db.py`, `profiles.py`):**
    * **AstraDB:** Cloud-native Cassandra database for persistence.
    * **Vector Search:** Used for retrieving relevant financial notes.
4.  **Langflow Workflows:**
    * *AskFinancialAdvisorV2:* Conditional routing between calculation tools and general advice.
    * *Budget Allocation Flow:* AI-powered logic for generating budget JSONs.

### Data Structure
<details>
<summary>Click to view User Profile JSON Structure</summary>

```json
{
    "id": 1,
    "general": {
        "name": "str",
        "age": "int",
        "monthly_income": "float",
        "current_savings": "float",
        "employment_status": "str",
        "debt_amount": "float",
        "dependents": "int"
    },
    "goals": ["Build Emergency Fund", "Pay Off Debt"],
    "budget": {
        "monthly_income": "int",
        "housing": "int",
        "food": "int",
        "transportation": "int",
        "savings": "int",
        "entertainment": "int",
        "miscellaneous": "int"
    }
}

```

</details>

---

## 🚀 Setup Instructions

### Prerequisites

* Python 3.8+
* AstraDB Account (Free tier available)
* Groq API Key (Free)
* OpenAI API Key (Optional - for Langflow integration)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd personal-finance-advisor

```


2. **Install dependencies**
```bash
pip install streamlit astrapy groq python-dotenv

```


3. **Database Setup (AstraDB)**
* Go to [DataStax Astra](https://astra.datastax.com) and create a new database.
* **Database Name:** `financial_advisor`
* **Keyspace:** `finance_data`
* **Provider/Region:** Choose your preferred cloud provider and region.
* Once active, click **"Generate Token"** and save the JSON file.


4. **Configure Environment Variables**
Create a `.env` file in the root directory:
```env
# AstraDB Configuration
ASTRA_DB_APPLICATION_TOKEN=AstraCS:...  # Your Token starting with AstraCS
ASTRA_DB_ID=your-db-id-here             # Found in database details
ASTRA_DB_REGION=us-east1                # Your selected region
ASTRA_DB_KEYSPACE=finance_data
ASTRA_ENDPOINT=https://<db-id>-<region>.apps.astra.datastax.com

# API Keys
GROQ_API_KEY=gsk_...                    # Your Groq API Key
OPENAI_API_KEY=sk-...                   # Optional: For Langflow

```


5. **Test Connection**
```bash
python test_connection.py

```



### Running the App

```bash
streamlit run main.py

```

---

## 📁 Project Structure

```text
financial-advisor/
├── main.py                 # Streamlit app entry point (Frontend)
├── ai.py                   # AI logic & Groq integration
├── db.py                   # AstraDB connection handler
├── profiles.py             # CRUD operations for User Profiles
├── form_submit.py          # Form submission handlers
├── test_connection.py      # Database connection tester
├── debug_connection.py     # Advanced DB debugging
├── prompts/                # Prompt Engineering
│   ├── conditional_router.txt
│   ├── general_agent.txt
│   ├── budget.txt
│   └── tool_calling_agent.txt
└── flows/                  # Langflow JSON exports
    ├── AskAIV2.json
    └── Budget Flow.json

```

---

## 🎨 Features

1. **Personal Financial Dashboard:** Track income, savings, debt, employment status, and dependents.
2. **Smart Goal Setting:** Choose from goals like *Build Emergency Fund*, *Pay Off Debt*, *Retirement*, or *Home Buying*.
3. **AI Budget Generator:**
* Generates breakdowns for Housing, Food, Transport, Savings, and Entertainment.
* Tailors recommendations based on income and location context.


4. **Intelligent Advisor:** Ask complex questions ("How can I save for a house with 50k income?") and get actionable advice.
5. **Vector Memory:** The app "remembers" your financial notes and retrieves them when relevant to your questions.

---

## 🧪 Testing & Debugging

* **Test Database:** Run `python test_connection.py` to verify AstraDB access.
* **Debug Mode:** Run `python debug_connection.py` for detailed logs.
* **Test AI Logic:**
```python
from ai import ask_ai
profile = {"general": {"monthly_income": 5000}}
print(ask_ai(profile, "How much should I save?"))

```



---

## 🚦 Roadmap

* [ ] Add visual expense tracking charts
* [ ] Implement investment portfolio analysis
* [ ] Add bill reminder notification system
* [ ] Multi-currency support
* [ ] PDF Export for financial reports

---


## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a PR.

## 📝 License

MIT License - feel free to use for personal or commercial projects.

```

```
