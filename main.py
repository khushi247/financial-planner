import streamlit as st
from ai import ask_ai_with_rag, get_budget
# 'get_notes' is correctly imported from profiles
from profiles import create_profile, get_notes, get_profile 
# 'update_personal_info' is correctly imported from form_submit
from form_submit import update_personal_info, add_note, delete_note

# Helper functions for safe data type conversion
def safe_int(value, default=5000):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=5000.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

st.title("Personal Finance & Budget Advisor")

@st.fragment()
def personal_data_form():
    with st.form("personal_data"):
        st.header("Personal Financial Data")

        profile = st.session_state.profile

        name = st.text_input("Name", value=profile["general"]["name"])
        age = st.number_input(
            "Age", 
            min_value=18, 
            max_value=100, 
            step=1, 
            value=safe_int(profile["general"]["age"], 30)
        )
        monthly_income = st.number_input(
            "Monthly Income ($)",
            min_value=0.0,
            max_value=1000000.0,
            step=100.0,
            value=safe_float(profile["general"]["monthly_income"], 5000.0),
        )
        current_savings = st.number_input(
            "Current Savings ($)",
            min_value=0.0,
            max_value=10000000.0,
            step=100.0,
            value=safe_float(profile["general"]["current_savings"], 10000.0),
        )
        employment_status = st.selectbox(
            "Employment Status",
            ["Full-time", "Part-time", "Self-employed", "Unemployed", "Retired"],
            index=["Full-time", "Part-time", "Self-employed", "Unemployed", "Retired"].index(
                profile["general"].get("employment_status", "Full-time")
            ),
        )
        debt_amount = st.number_input(
            "Total Debt ($)",
            min_value=0.0,
            max_value=1000000.0,
            step=100.0,
            value=safe_float(profile["general"]["debt_amount"], 0.0),
        )
        dependents = st.number_input(
            "Number of Dependents",
            min_value=0,
            max_value=20,
            step=1,
            value=safe_int(profile["general"]["dependents"], 0),
        )

        personal_data_submit = st.form_submit_button("Save")
        if personal_data_submit:
            if all([name, age, monthly_income is not None]):
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                        profile,
                        "general",
                        name=name,
                        age=age,
                        monthly_income=monthly_income,
                        current_savings=current_savings,
                        employment_status=employment_status,
                        debt_amount=debt_amount,
                        dependents=dependents,
                    )
                    st.success("Information saved.")
            else:
                st.warning("Please fill in all required fields!")

@st.fragment()
def goals_form():
    profile = st.session_state.profile
    with st.form("goals_form"):
        st.header("Financial Goals")
        goals = st.multiselect(
            "Select your Financial Goals",
            ["Build Emergency Fund", "Pay Off Debt", "Save for Retirement", "Buy a Home", "Investment Growth"],
            default=profile.get("goals", ["Build Emergency Fund"]),
        )

        goals_submit = st.form_submit_button("Save")
        if goals_submit:
            if goals:
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                        profile, "goals", goals=goals
                    )
                    st.success("Goals updated")
            else:
                st.warning("Please select at least one goal.")

@st.fragment()
def budget_allocation():
    profile = st.session_state.profile
    budget_container = st.container(border=True)
    budget_container.header("Budget Allocation")
    if budget_container.button("Generate with AI"):
        # Pass the 'general' profile data to get_budget, which includes the correct income
        result = get_budget(profile.get("general"), profile.get("goals"))
        profile["budget"] = result
        # Also update the 'budget' section in the database
        st.session_state.profile = update_personal_info(
            profile,
            "budget",
            **result # Unpack the entire budget dict to save it
        )
        budget_container.success("AI has generated the budget.")

    with budget_container.form("budget_form", border=False):
        
        # Display the single source of truth for income. Do not make it editable here.
        income_display = profile.get("general", {}).get("monthly_income", 0)
        st.info(f"Budget is based on your Monthly Income: **${income_display:,.0f}**")

        col1, col2 = st.columns(2)
        with col1:
            housing = st.number_input(
                "Housing ($)",
                min_value=0,
                step=50,
                value=safe_int(profile["budget"].get("housing", 0), 0),
            )
            food = st.number_input(
                "Food ($)",
                min_value=0,
                step=50,
                value=safe_int(profile["budget"].get("food", 0), 0),
            )
            transportation = st.number_input(
                "Transportation ($)",
                min_value=0,
                step=50,
                value=safe_int(profile["budget"].get("transportation", 0), 0),
            )
        with col2:
            savings = st.number_input(
                "Savings ($)",
                min_value=0,
                step=50,
                value=safe_int(profile["budget"].get("savings", 0), 0),
            )
            entertainment = st.number_input(
                "Entertainment ($)",
                min_value=0,
                step=50,
                value=safe_int(profile["budget"].get("entertainment", 0), 0),
            )
            miscellaneous = st.number_input(
                "Miscellaneous ($)",
                min_value=0,
                step=50,
                value=safe_int(profile["budget"].get("miscellaneous", 0), 0),
            )

        if st.form_submit_button("Save"):
            with st.spinner():
                st.session_state.profile = update_personal_info(
                    profile,
                    "budget",
                    housing=housing,
                    food=food,
                    transportation=transportation,
                    savings=savings,
                    entertainment=entertainment,
                    miscellaneous=miscellaneous,
                )
                st.success("Budget saved")

@st.fragment()
def notes():
    st.subheader("Financial Notes (For RAG):")
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5, 1])
        with cols[0]:
            st.text(note.get("text"))
        with cols[1]:
            if st.button("Delete", key=i):
                delete_note(note.get("_id"))
                st.session_state.notes.pop(i)
                st.rerun()
    
    new_note = st.text_input("Add a financial note (e.g., 'I tend to overspend on credit cards'):")
    if st.button("Add Note"):
        if new_note:
            note = add_note(new_note, st.session_state.profile_id)
            st.session_state.notes.append(note)
            st.rerun()

# @st.fragment()
# def ask_ai_func():
#     st.subheader('💬 Ask Financial Advisor AI (RAG System)')
    
#     # RAG System Explanation
#     with st.expander("🔍 How RAG Works in This App"):
#         st.markdown("""
#         **Retrieval-Augmented Generation (RAG) Pipeline:**
        
#         1. **📥 Retrieval**: Your question is converted to a vector embedding and compared against stored financial notes in the vector database.
#         2. **🔗 Augmentation**: Retrieved notes are combined with your profile data to create enriched context.
#         3. **🤖 Generation**: AI generates personalized advice using the augmented context.
        
#         **Try it:** Add notes about your financial habits, then ask related questions!
#         """)
    
#     # Sample questions for inspiration
#     with st.expander("💡 Example Questions to Test RAG"):
#         st.markdown("""
#         - What should I do about the credit card issue I mentioned?
#         - Based on my investment notes, what's my next step?
#         - How can I improve the budgeting strategy I wrote about?
#         - What actions should I take on my savings goals?
#         """)
    
#     user_question = st.text_input("Ask a financial question:", placeholder="e.g., What should I do about my investment portfolio?")
    
#     if st.button("🚀 Ask AI with RAG", type="primary"):
#         if not user_question:
#             st.warning("Please enter a question first!")
#         else:
#             with st.spinner("🔄 Running RAG Pipeline..."):
#                 # Call the complete RAG system
#                 rag_result = ask_ai_with_rag(
#                     st.session_state.profile, 
#                     user_question,
#                     st.session_state.profile_id
#                 )
                
#                 # Check the retrieval method and warn user if RAG is not working
#                 method = rag_result["rag_pipeline"]["retrieval"]["method"]
#                 if method != "vector_search":
#                     st.warning(
#                         f"⚠️ **Vector Search Not Active!** The app is using a '{method}' fallback. "
#                         "AI answers will only be based on your profile and simple keyword matches, "
#                         "not semantic meaning. Check your AstraDB vector configuration.", 
#                         icon="🔥"
#                     )

#                 # Display RAG Pipeline Visualization
#                 st.markdown("---")
#                 st.markdown("### 🔄 RAG Pipeline Execution")
                
#                 col1, col2, col3 = st.columns(3)
                
#                 with col1:
#                     st.metric(
#                         "📥 Retrieved Docs", 
#                         rag_result["rag_pipeline"]["retrieval"]["num_documents"],
#                         help="Number of relevant notes found in vector DB"
#                     )
                
#                 with col2:
#                     st.metric(
#                         "🔗 Context Added", 
#                         "Yes" if rag_result["rag_pipeline"]["augmentation"]["has_context"] else "No",
#                         help="Whether retrieved context was added to prompt"
#                     )
                
#                 with col3:
#                     st.metric(
#                         "🤖 Model Used", 
#                         "Llama 3.3 70B",
#                         help="LLM used for generation"
#                     )
                
#                 # Show Retrieved Documents (RAG Transparency)
#                 if rag_result["rag_pipeline"]["retrieval"]["num_documents"] > 0:
#                     with st.expander("📚 Retrieved Context (What RAG Found)", expanded=True):
#                         st.markdown("**These notes were retrieved from the vector database based on semantic similarity:**")
                        
#                         for i, doc in enumerate(rag_result["rag_pipeline"]["retrieval"]["documents"], 1):
#                             similarity = doc.get("similarity_score", 0)
#                             text = doc.get("text", "")
                            
#                             # Color code based on relevance
#                             if similarity > 0.8:
#                                 color = "#4CAF50"  # Green - highly relevant
#                             elif similarity > 0.6:
#                                 color = "#FF9800"  # Orange - moderately relevant
#                             else:
#                                 color = "#9E9E9E"  # Gray - less relevant
                            
#                             st.markdown(
#                                 f"""
#                                 <div style="
#                                     border-left: 4px solid {color};
#                                     padding: 10px;
#                                     margin: 10px 0;
#                                     background-color: #f9f9f9;
#                                 ">
#                                     <strong>Note {i}</strong> (Similarity: {similarity:.2%})<br>
#                                     {text}
#                                 </div>
#                                 """,
#                                 unsafe_allow_html=True
#                             )
#                 else:
#                     st.info("ℹ️ No relevant notes found. AI will use only your profile data. Add more notes to improve RAG!")
                
#                 # Display AI Response
#                 st.markdown("---")
#                 st.markdown("### 💡 AI Financial Advice (Generated)")
                
#                 # --- THIS IS THE FIX ---
#                 #
#                 # By using `st.container(border=True)` and passing the raw
#                 # response to `st.markdown()`, Streamlit will correctly
#                 # render the bolding, lists, and paragraphs.
#                 #
#                 # We remove the custom HTML `div` and the `.replace('\n', '<br>')`
                
#                 with st.container(border=True):
#                     st.markdown(rag_result["response"])
                
#                 # --- END FIX ---
                
                
#                 # Show full RAG pipeline details (for debugging/transparency)
#                 with st.expander("🔧 RAG Pipeline Technical Details"):
#                     st.json(rag_result["rag_pipeline"])
                
#                 # Show profile context
#                 st.markdown("---")
#                 with st.expander("📊 Your Current Financial Profile", expanded=False):
#                     col1, col2, col3, col4 = st.columns(4)
#                     with col1:
#                         income_val = st.session_state.profile['general'].get('monthly_income', 0)
#                         st.metric("Monthly Income", "${:,.0f}".format(income_val))
#                     with col2:
#                         savings_val = st.session_state.profile['general'].get('current_savings', 0)
#                         st.metric("Current Savings", "${:,.0f}".format(savings_val))
#                     with col3:
#                         debt_val = st.session_state.profile['general'].get('debt_amount', 0)
#                         st.metric("Total Debt", "${:,.0f}".format(debt_val))
#                     with col4:
#                         monthly_savings = st.session_state.profile['budget'].get('savings', 0)
#                         st.metric("Monthly Savings", "${:,.0f}".format(monthly_savings))
                    
#                     # Show budget breakdown
#                     st.markdown("#### 📈 Current Budget Breakdown")
#                     budget = st.session_state.profile.get('budget', {})
#                     budget_df_data = {
#                         'Category': ['Housing', 'Food', 'Transportation', 'Savings', 'Entertainment', 'Miscellaneous'],
#                         'Amount': [
#                             "${:,}".format(budget.get('housing', 0)),
#                             "${:,}".format(budget.get('food', 0)),
#                             "${:,}".format(budget.get('transportation', 0)),
#                             "${:,}".format(budget.get('savings', 0)),
#                             "${:,}".format(budget.get('entertainment', 0)),
#                             "${:,}".format(budget.get('miscellaneous', 0))
#                         ]
#                     }
#                     st.table(budget_df_data)
@st.fragment()
def ask_ai_func():
    st.subheader('💬 Ask Financial Advisor AI (RAG System)')
    
    # RAG System Explanation
    with st.expander("🔍 How RAG Works in This App"):
        st.markdown("""
        **Retrieval-Augmented Generation (RAG) Pipeline:**
        
        1. **📥 Retrieval**: Your question is converted to a vector embedding and compared against stored financial notes in the vector database
        2. **🔗 Augmentation**: Retrieved notes are combined with your profile data to create enriched context
        3. **🤖 Generation**: AI generates personalized advice using the augmented context
        
        **Try it:** Add notes about your financial habits, then ask related questions!
        """)
    
    # Sample questions for inspiration
    with st.expander("💡 Example Questions to Test RAG"):
        st.markdown("""
        - What should I do about the credit card issue I mentioned?
        - Based on my investment notes, what's my next step?
        - How can I improve the budgeting strategy I wrote about?
        - What actions should I take on my savings goals?
        """)
    
    user_question = st.text_input("Ask a financial question:", placeholder="e.g., What should I do about my investment portfolio?")
    
    if st.button("🚀 Ask AI with RAG", type="primary"):
        if not user_question:
            st.warning("Please enter a question first!")
        else:
            with st.spinner("🔄 Running RAG Pipeline..."):
                # Call the complete RAG system
                rag_result = ask_ai_with_rag(
                    st.session_state.profile, 
                    user_question,
                    st.session_state.profile_id
                )
                
                # Check the retrieval method and warn user if RAG is not working
                method = rag_result["rag_pipeline"]["retrieval"]["method"]
                if method != "vector_search":
                    st.warning(
                        f"⚠️ **Vector Search Not Active!** The app is using a '{method}' fallback. "
                        "AI answers will only be based on your profile and simple keyword matches, "
                        "not semantic meaning. Check your AstraDB vector configuration.", 
                        icon="🔥"
                    )

                # Display RAG Pipeline Visualization
                st.markdown("---")
                st.markdown("### 🔄 RAG Pipeline Execution")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "📥 Retrieved Docs", 
                        rag_result["rag_pipeline"]["retrieval"]["num_documents"],
                        help="Number of relevant notes found in vector DB"
                    )
                
                with col2:
                    st.metric(
                        "🔗 Context Added", 
                        "Yes" if rag_result["rag_pipeline"]["augmentation"]["has_context"] else "No",
                        help="Whether retrieved context was added to prompt"
                    )
                
                with col3:
                    st.metric(
                        "🤖 Model Used", 
                        "Llama 3.3 70B",
                        help="LLM used for generation"
                    )
                
                # Show Retrieved Documents (RAG Transparency)
                if rag_result["rag_pipeline"]["retrieval"]["num_documents"] > 0:
                    with st.expander("📚 Retrieved Context (What RAG Found)", expanded=True):
                        st.markdown("**These notes were retrieved from the vector database based on semantic similarity:**")
                        
                        for i, doc in enumerate(rag_result["rag_pipeline"]["retrieval"]["documents"], 1):
                            similarity = doc.get("similarity_score", 0)
                            text = doc.get("text", "")
                            
                            # Color code based on relevance
                            if similarity > 0.8:
                                color = "#4CAF50"  # Green - highly relevant
                            elif similarity > 0.6:
                                color = "#FF9800"  # Orange - moderately relevant
                            else:
                                color = "#9E9E9E"  # Gray - less relevant
                            
                            st.markdown(
                                f"""
                                <div style="
                                    border-left: 4px solid {color};
                                    padding: 10px;
                                    margin: 10px 0;
                                    background-color: #f9f9f9;
                                ">
                                    <strong>Note {i}</strong> (Similarity: {similarity:.2%})<br>
                                    {text}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                else:
                    st.info("ℹ️ No relevant notes found. AI will use only your profile data. Add more notes to improve RAG!")
                
                # Display AI Response
                st.markdown("---")
                st.markdown("### 💡 AI Financial Advice (Generated)")
                
                # --- FIX: Use Streamlit container for clean formatting ---
                with st.container(border=True):
                    # Simply pass the raw response for perfect Markdown rendering
                    st.markdown(rag_result["response"]) 
                # --- END FIX ---
                
                
                # Show full RAG pipeline details (for debugging/transparency)
                with st.expander("🔧 RAG Pipeline Technical Details"):
                    st.json(rag_result["rag_pipeline"])
                
                # Show profile context
                st.markdown("---")
                with st.expander("📊 Your Current Financial Profile", expanded=False):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        income_val = st.session_state.profile['general'].get('monthly_income', 0)
                        st.metric("Monthly Income", "${:,.0f}".format(income_val))
                    with col2:
                        savings_val = st.session_state.profile['general'].get('current_savings', 0)
                        st.metric("Current Savings", "${:,.0f}".format(savings_val))
                    with col3:
                        debt_val = st.session_state.profile['general'].get('debt_amount', 0)
                        st.metric("Total Debt", "${:,.0f}".format(debt_val))
                    with col4:
                        monthly_savings = st.session_state.profile['budget'].get('savings', 0)
                        st.metric("Monthly Savings", "${:,.0f}".format(monthly_savings))
                    
                    # Show budget breakdown
                    st.markdown("#### 📈 Current Budget Breakdown")
                    budget = st.session_state.profile.get('budget', {})
                    budget_df_data = {
                        'Category': ['Housing', 'Food', 'Transportation', 'Savings', 'Entertainment', 'Miscellaneous'],
                        'Amount': [
                            "${:,}".format(budget.get('housing', 0)),
                            "${:,}".format(budget.get('food', 0)),
                            "${:,}".format(budget.get('transportation', 0)),
                            "${:,}".format(budget.get('savings', 0)),
                            "${:,}".format(budget.get('entertainment', 0)),
                            "${:,}".format(budget.get('miscellaneous', 0))
                        ]
                    }
                    st.table(budget_df_data)

def forms():
    if "profile" not in st.session_state:
        # --- NO CHANGE HERE: Still fine for a demo ---
        profile_id = 1 
        profile = get_profile(profile_id)
        if not profile:
            profile_id, profile = create_profile(profile_id)

        st.session_state.profile = profile
        st.session_state.profile_id = profile_id

    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)

    personal_data_form()
    goals_form()
    budget_allocation()
    notes()
    ask_ai_func()

if __name__ == "__main__":
    forms()