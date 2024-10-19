import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import json

# Load translations from a JSON file (English is default)
def load_translations(language):
    try:
        with open('translations.json',encoding='utf-8') as f:
            translations = json.load(f)
        return translations.get(language, translations['en'])
    except FileNotFoundError:
        st.error("Translation file not found. Defaulting to English.")
        return translations['en']

# Function to translate text based on selected language
def translate(key, translations):
    return translations.get(key, key)

# Sidebar for language selection
st.sidebar.title('🌍 Language Selection')
language = st.sidebar.selectbox("Choose language:", ['English', 'Twi','Ga','Hausa'])
language_key = {"English": "en", "Twi": "twi", "Ga":"ga","Hausa":"ha"}[language]

# Load translations for the selected language
translations = load_translations(language_key)

# Custom CSS for a modern UI
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f4f8;
        color: #333;
    }
    h1 {
        color: #2c3e50;
        font-size: 2.5em;
    }
    h2 {
        color: #34495e;
    }
    .stButton>button {
        background-color: #2980b9;
        color: white;
        border: None;
        border-radius: 5px;
        padding: 10px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1a6f9a;
    }
    .metric {
        font-size: 24px;
        color: #27ae60;
    }
    .sidebar .sidebar-content {
        padding: 10px;
    }
    .sidebar .stButton {
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
st.sidebar.title(f"🔑 {translate('financial_dashboard_navigation', translations)}")
st.sidebar.write(translate('navigation_instructions', translations))
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# Button to navigate to Dashboard
if st.sidebar.button(translate('navigate_dashboard', translations)):
    st.session_state.page = "Dashboard"

# Button to navigate to Graphs
if st.sidebar.button(translate('navigate_graphs', translations)):
    st.session_state.page = "Graphs"


# Initialize session state for financial metrics if not already done
if 'current_balance' not in st.session_state:
    st.session_state.current_balance = 1200  # Default current balance
if 'total_savings' not in st.session_state:
    st.session_state.total_savings = 5000  # Default total savings
if 'investment_value' not in st.session_state:
    st.session_state.investment_value = 10000  # Default investment value
if 'expenses' not in st.session_state:
    st.session_state.expenses = []  # Initialize empty list for expenses

if st.session_state.page == "Dashboard":
    # Title and Header
    st.title(f"💰 {translate('dashboard_title', translations)}")
    st.header(f"📊 {translate('overview_title', translations)}")

    # Financial Metrics Input
    st.subheader(f"💸 {translate('update_metrics', translations)}")
    st.session_state.current_balance = st.number_input(translate('current_balance', translations), min_value=0, value=st.session_state.current_balance)
    st.session_state.total_savings = st.number_input(translate('total_savings', translations), min_value=0, value=st.session_state.total_savings)
    st.session_state.investment_value = st.number_input(translate('investment_value', translations), min_value=0, value=st.session_state.investment_value)

    # Financial Metrics Display
    st.subheader(f"📈 {translate('key_metrics', translations)}")
    col1, col2, col3 = st.columns(3)
    col1.metric(translate('current_balance', translations), f"GHS {st.session_state.current_balance}")
    col2.metric(translate('total_savings', translations), f"GHS {st.session_state.total_savings}")
    col3.metric(translate('investment_value', translations), f"GHS {st.session_state.investment_value}")

    # Financial Goals Section
    st.subheader(f"🎯 {translate('set_goals', translations)}")
    goal = st.selectbox(translate('choose_goal_1', translations), [
    translate('emergency_fund', translations), 
    translate('home_purchase', translations), 
    translate('retirement', translations), 
    translate('debt_repayment', translations)
])

    goal_amount = st.number_input(translate('goal_amount', translations), min_value=0, value=1000)

    # Financial Goals Explanation
    if goal == 'Emergency Fund':
        st.write(f"💡 {translate('emergency_fund_suggestion', translations)}")
    elif goal == 'Home Purchase':
        st.write(f"🏡 {translate('home_purchase_suggestion', translations)}")
    elif goal == 'Retirement':
        st.write(f"📅 {translate('retirement_suggestion', translations)}")
    else:
        st.write(f"🚀 {translate('debt_repayment_suggestion', translations)}")

    # Suggestions based on the financial goal
    st.write(translate('goal_suggestions_intro', translations))
    if goal == 'Emergency Fund':
        st.write(translate('emergency_fund_tip', translations))
    elif goal == 'Home Purchase':
        st.write(translate('home_purchase_tip', translations))

    # Expense Tracking Section
    st.subheader(f"📝 {translate('track_expenses', translations)}")
    with st.form("expense_form"):
        expense_name = st.text_input(translate('add_expense', translations), 'Rent')
        expense_amount = st.number_input(translate('total_expenses', translations), min_value=0, max_value=10000, value=1000)
        add_expense = st.form_submit_button(f"➕ {translate('add_expense', translations)}")

    # Add expense to session state
    if add_expense:
        st.session_state.expenses.append({'name': expense_name, 'amount': expense_amount})
        st.success(f"✅ {translate('add_expense', translations)} {expense_name} with amount GHS {expense_amount}")

    # Display expenses
    if st.session_state.expenses:
        st.subheader(f"📋 {translate('total_expenses', translations)}")
        expense_df = pd.DataFrame(st.session_state.expenses)
        st.table(expense_df)
        st.metric(translate('total_expenses', translations), f"GHS {expense_df['amount'].sum()}")

    # Monthly Budget Progress
    st.subheader(f"📊 {translate('budget_progress', translations)}")
    monthly_income = st.slider('Enter your monthly income (GHS)', 500, 10000, 2000)
    total_expenses = expense_df['amount'].sum() if st.session_state.expenses else 0
    budget_remaining = monthly_income - total_expenses
    st.progress(budget_remaining / monthly_income)

    # Financial Health Score
    st.subheader(f"🏆 {translate('financial_health_score', translations)}")
    health_score = min(100, max(0, ((st.session_state.total_savings + st.session_state.investment_value - total_expenses) / monthly_income) * 10))
    st.metric(translate('financial_health_score', translations), f"{health_score}/100")

elif st.session_state.page == "Graphs":
    st.title(f"📊 {translate('financial_graphs', translations)}")
    st.subheader(f"📈 {translate('balance_over_time', translations)}")

    # Generate sample data for the graph
    months = pd.date_range(start='2023-01-01', periods=12, freq='M')
    balances = np.random.randint(1000, 5000, size=12)

    # Plotly line chart
    fig = go.Figure([go.Scatter(x=months, y=balances, mode='lines+markers')])
    fig.update_layout(title=translate('balance_over_time', translations), xaxis_title="Month", yaxis_title="Balance (GHS)")
    st.plotly_chart(fig)

    # Expense Breakdown Chart
    st.subheader(f"📊 {translate('expense_breakdown', translations)}")
    if st.session_state.expenses:
        expense_breakdown_fig = go.Figure([go.Pie(labels=expense_df['name'], values=expense_df['amount'])])
        st.plotly_chart(expense_breakdown_fig)
    else:
        st.write("No expenses added yet.")

    # Savings vs Investment Chart
    st.subheader(f"📊 {translate('savings_investment_comparison', translations)}")
    comparison_fig = go.Figure()
    comparison_fig.add_trace(go.Bar(x=['Savings', 'Investments'], y=[st.session_state.total_savings, st.session_state.investment_value]))
    st.plotly_chart(comparison_fig)
