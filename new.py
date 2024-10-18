import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

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
st.sidebar.title('🔑 Financial Dashboard Navigation')
st.sidebar.write("Use the buttons below to navigate through the app:")
# Store the selected page in session state
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# Button to navigate to Dashboard
if st.sidebar.button('Dashboard'):
    st.session_state.page = "Dashboard"

# Button to navigate to Graphs
if st.sidebar.button('Graphs'):
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
    st.title('💰 Personal Financial Dashboard')
    st.header('📊 Overview of Your Financial Health')

    # Financial Metrics Input
    st.subheader('💸 Update Your Financial Metrics')
    st.session_state.current_balance = st.number_input('Current Balance (GHS)', min_value=0, value=st.session_state.current_balance)
    st.session_state.total_savings = st.number_input('Total Savings (GHS)', min_value=0, value=st.session_state.total_savings)
    st.session_state.investment_value = st.number_input('Investment Value (GHS)', min_value=0, value=st.session_state.investment_value)

    # Financial Metrics Display
    st.subheader('📈 Key Financial Metrics')
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Balance", f"GHS {st.session_state.current_balance}")
    col2.metric("Total Savings", f"GHS {st.session_state.total_savings}")
    col3.metric("Investment Value", f"GHS {st.session_state.investment_value}")

    # Financial Goals Section
    st.subheader('🎯 Set Your Financial Goals')
    goal = st.selectbox('Choose a financial goal:', ['Emergency Fund', 'Home Purchase', 'Retirement', 'Debt Repayment'])
    goal_amount = st.number_input('Enter your goal amount (GHS)', min_value=0, value=1000)

    # Financial Goals Explanation
    if goal == 'Emergency Fund':
        st.write('💡 You need to save at least 3-6 months of living expenses.')
    elif goal == 'Home Purchase':
        st.write('🏡 You should aim to save for a down payment (typically 20% of the home value).')
    elif goal == 'Retirement':
        st.write('📅 Consider saving 15% of your income towards retirement.')
    else:
        st.write('🚀 Focus on paying off high-interest debt first.')

    # Expense Tracking Section
    st.subheader('📝 Track Your Expenses')
    with st.form("expense_form"):
        expense_name = st.text_input('Expense Name', 'Rent')
        expense_amount = st.number_input('Expense Amount (GHS)', min_value=0, max_value=10000, value=1000)
        add_expense = st.form_submit_button('➕ Add Expense')

    # Add expense to session state
    if add_expense:
        st.session_state.expenses.append({'name': expense_name, 'amount': expense_amount})
        st.success(f'✅ Added {expense_name} with amount GHS {expense_amount}')

    # Display expenses
    if st.session_state.expenses:
        st.subheader('📋 Your Expenses')
        expense_df = pd.DataFrame(st.session_state.expenses)
        st.table(expense_df)
        st.metric("Total Expenses", f"GHS {expense_df['amount'].sum()}")

    # Monthly Budget Progress
    st.subheader('📊 Monthly Budget Progress')
    monthly_income = st.slider('Enter your monthly income (GHS)', 500, 10000, 2000)
    total_expenses = expense_df['amount'].sum() if st.session_state.expenses else 0
    budget_remaining = monthly_income - total_expenses
    st.progress(budget_remaining / monthly_income)

    # Savings & Investment Advice
    st.subheader('💡 Savings and Investment Suggestions')
    st.write('Based on your goal and current balance, here are some suggestions:')
    if goal == 'Emergency Fund':
        st.write('🌟 Try to save GHS 500 more this month to reach your goal faster.')
    elif goal == 'Home Purchase':
        st.write('💼 Invest in a high-yield savings account or consider low-risk investments.')

    # Financial Health Score
    st.subheader('🏆 Your Financial Health Score')
    health_score = min(100, max(0, ((st.session_state.current_balance + st.session_state.total_savings) / (monthly_income + 1)) * 100))
    st.metric("Financial Health Score", f"{int(health_score)}/100")

elif st.session_state.page == "Graphs":
    st.title('📊 Financial Graphs')
    
    # Graph: Balance Over Time
    st.subheader('📈 Balance Over Time')
    # Placeholder for actual balance data
    dates = pd.date_range(start="2023-01-01", periods=12, freq='M')
    # Using session state to simulate balance over time
    balances = np.random.randint(1000, 2000, size=12).tolist()  # Replace with real data fetching logic

    # Create a line graph of balance over time
    balance_trace = go.Scatter(x=dates, y=balances, mode='lines+markers', name='Balance')
    layout = go.Layout(title='Current Balance Over Time', xaxis_title='Month', yaxis_title='Balance (GHS)')
    fig = go.Figure(data=[balance_trace], layout=layout)
    st.plotly_chart(fig)

    # Graph: Expense Breakdown
    if st.session_state.expenses:
        st.subheader('📊 Expense Breakdown')
        expense_df = pd.DataFrame(st.session_state.expenses)
        expense_breakdown = expense_df.groupby('name').sum().reset_index()

        pie_fig = go.Figure(data=[go.Pie(labels=expense_breakdown['name'], values=expense_breakdown['amount'], hole=.3)])
        pie_fig.update_layout(title_text='Expenses by Category')
        st.plotly_chart(pie_fig)

    # Graph: Savings Progress
    st.subheader('🏦 Savings Progress')
    goal_amount = 5000
    current_savings = st.session_state.total_savings  # Fetching actual savings from session state
    savings_progress = current_savings / goal_amount
    bar_fig = go.Figure(data=[go.Bar(x=['Savings Progress'], y=[savings_progress], marker_color='green')])
    bar_fig.update_layout(title='Progress Towards Savings Goal', yaxis=dict(tickvals=[0, 1], ticktext=['0%', '100%']), yaxis_title='Progress', xaxis_title='Goal')
    st.plotly_chart(bar_fig)

    # Educational Module
    st.subheader('📚 Financial Literacy Tips')
    with st.expander('What is Compound Interest?'):
        st.write('🔍 Compound interest is the interest on a loan or deposit calculated based on both the initial principal and the accumulated interest from previous periods.')

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.write("### © 2024 Personal Finance Dashboard. All rights reserved.")
