import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import json

# Load translations from the JSON file
# Load translations from the JSON file with UTF-8 encoding
with open('translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)


# Language selection
language = st.sidebar.selectbox("🌍 Select Language", options=["English", "French", "Spanish"])

# Helper function to get the translation
def translate(key):
    return translations[language].get(key, key)

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
st.sidebar.title(translate("title"))
st.sidebar.write(translate("use_buttons_to_navigate"))

if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# Button to navigate to Dashboard
if st.sidebar.button(translate('dashboard')):
    st.session_state.page = "Dashboard"

# Button to navigate to Graphs
if st.sidebar.button(translate('graphs')):
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

# Dashboard Page
if st.session_state.page == "Dashboard":
    st.title(translate("title"))
    st.header(translate("header"))

    # Financial Metrics Input
    st.subheader(translate("update_metrics"))
    st.session_state.current_balance = st.number_input(translate("current_balance"), min_value=0, value=st.session_state.current_balance)
    st.session_state.total_savings = st.number_input(translate("total_savings"), min_value=0, value=st.session_state.total_savings)
    st.session_state.investment_value = st.number_input(translate("investment_value"), min_value=0, value=st.session_state.investment_value)

    # Financial Metrics Display
    st.subheader(translate("key_financial_metrics"))
    col1, col2, col3 = st.columns(3)
    col1.metric(translate("current_balance"), f"GHS {st.session_state.current_balance}")
    col2.metric(translate("total_savings"), f"GHS {st.session_state.total_savings}")
    col3.metric(translate("investment_value"), f"GHS {st.session_state.investment_value}")

    # Financial Goals Section
    st.subheader(translate("set_financial_goals"))
    goal = st.selectbox(translate('choose_goal'), ['Emergency Fund', 'Home Purchase', 'Retirement', 'Debt Repayment'])
    goal_amount = st.number_input(translate("goal_amount"), min_value=0, value=1000)

    # Financial Goals Explanation
    if goal == 'Emergency Fund':
        st.write(translate('emergency_fund_tip'))
    elif goal == 'Home Purchase':
        st.write(translate('home_purchase_tip'))
    elif goal == 'Retirement':
        st.write(translate('retirement_tip'))
    else:
        st.write(translate('debt_repayment_tip'))

    # Expense Tracking Section
    st.subheader(translate('expense_tracking'))
    with st.form("expense_form"):
        expense_name = st.text_input(translate('expense_name'), 'Rent')
        expense_amount = st.number_input(translate('expense_amount'), min_value=0, max_value=10000, value=1000)
        add_expense = st.form_submit_button(translate('add_expense'))

    # Add expense to session state
    if add_expense:
        st.session_state.expenses.append({'name': expense_name, 'amount': expense_amount})
        st.success(f"✅ {translate('added_expense')} {expense_name} ({expense_amount} GHS)")

    # Display expenses
    if st.session_state.expenses:
        st.subheader(translate('your_expenses'))
        expense_df = pd.DataFrame(st.session_state.expenses)
        st.table(expense_df)
        st.metric(translate('total_expenses'), f"GHS {expense_df['amount'].sum()}")

    # Monthly Budget Progress
    st.subheader(translate('monthly_budget_progress'))
    monthly_income = st.slider(translate('monthly_income'), 500, 10000, 2000)
    total_expenses = expense_df['amount'].sum() if st.session_state.expenses else 0
    budget_remaining = monthly_income - total_expenses
    st.progress(budget_remaining / monthly_income)

    # Savings & Investment Advice
    st.subheader(translate('savings_investment_advice'))
    st.write(translate('suggestion_based_on_goal'))
    if goal == 'Emergency Fund':
        st.write(translate('emergency_fund_suggestion'))
    elif goal == 'Home Purchase':
        st.write(translate('home_purchase_suggestion'))

    # Financial Health Score
    st.subheader(translate('financial_health_score'))
    health_score = min(100, max(0, ((st.session_state.current_balance + st.session_state.total_savings) / (monthly_income + 1)) * 100))
    st.metric(translate('financial_health_score'), f"{int(health_score)}/100")

# Graphs Page
elif st.session_state.page == "Graphs":
    st.title(translate('graphs'))

    # Graph: Balance Over Time
    st.subheader(translate('balance_over_time'))
    dates = pd.date_range(start="2023-01-01", periods=12, freq='M')
    balances = np.random.randint(1000, 2000, size=12).tolist()  # Replace with real data fetching logic

    balance_trace = go.Scatter(x=dates, y=balances, mode='lines+markers', name=translate('balance'))
    layout = go.Layout(title=translate('balance_over_time'), xaxis_title=translate('month'), yaxis_title=translate('balance'))
    fig = go.Figure(data=[balance_trace], layout=layout)
    st.plotly_chart(fig)

    # Graph: Expense Breakdown
    if st.session_state.expenses:
        st.subheader(translate('expense_breakdown'))
        expense_df = pd.DataFrame(st.session_state.expenses)
        expense_breakdown = expense_df.groupby('name').sum().reset_index()

        pie_fig = go.Figure(data=[go.Pie(labels=expense_breakdown['name'], values=expense_breakdown['amount'], hole=.3)])
        pie_fig.update_layout(title_text=translate('expense_by_category'))
        st.plotly_chart(pie_fig)

    # Graph: Savings Progress
    st.subheader(translate('savings_progress'))
    goal_amount = 5000
    current_savings = st.session_state.total_savings
    savings_progress = current_savings / goal_amount
    bar_fig = go.Figure(data=[go.Bar(x=[translate('savings_progress')], y=[savings_progress], marker_color='green')])
    bar_fig.update_layout(title=translate('savings_goal_progress'), yaxis=dict(tickvals=[0, 1], ticktext=['0%', '100%']), yaxis_title=translate('progress'), xaxis_title=translate('goal'))
    st.plotly_chart(bar_fig)

    # Educational Module
    st.subheader(translate('financial_literacy_tips'))
    with st.expander(translate('compound_interest_explained')):
        st.write(translate('compound_interest_definition'))

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.write(f"### © 2024 {translate('footer')}")
