import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import functions as py  # Import the functions module
import transform as t

# Set Streamlit page configuration
st.set_page_config(page_title="Automated Financial Report Analysis Tool", page_icon="📊", layout="wide")

# Sidebar Content - Helpful Links and Contact Information
st.sidebar.header("📜 Resources")
st.sidebar.markdown("[Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)")
st.sidebar.markdown("[Streamlit Documentation](https://docs.streamlit.io/)")
st.sidebar.header("📞 Contact Us")
st.sidebar.info("For any questions, feel free to reach out at [your.email@example.com](mailto:your.email@example.com)")

# Streamlit App Title and Image
st.title("📊 Automated Financial Report Analysis Tool")
st.caption("Analyze the financial report of a company using Streamlit and Python.")
st.image("https://example.com/financial_analysis_image.jpg", caption="Financial Analysis Made Simple")  # Placeholder image

# User Input Section
st.header("🔍 Company Financial Data Analysis")
st.caption("Enter a valid company symbol and click the button to analyze the data.")
company_symbol = st.text_input("Enter Company Symbol:", value="MSFT")

# Initialize session states to store data
if 'financial_data_loaded' not in st.session_state:
    st.session_state['financial_data_loaded'] = False
if 'pnl_concat' not in st.session_state:
    st.session_state['pnl_concat'] = None
if 'bs_concat' not in st.session_state:
    st.session_state['bs_concat'] = None
if 'cf_concat' not in st.session_state:
    st.session_state['cf_concat'] = None
if 'selected_year' not in st.session_state:
    st.session_state['selected_year'] = None
if 'insights_generated' not in st.session_state:
    st.session_state['insights_generated'] = False

# Button to trigger data retrieval and processing
if st.button("💼 Get Financial Data"):
    try:
        # Load the data (testing with CSV data as placeholder for now)
        bs_annual = pd.read_csv("Data/bs_annual_MSFT.csv")
        cf_annual = pd.read_csv("Data/cf_annual_MSFT.csv")
        pnl_annual = pd.read_csv("Data/pnl_annual_MSFT.csv")

        # Clean and process the data
        bs_annual, pnl_annual, cf_annual = t.clean_dataframes(bs_annual, pnl_annual, cf_annual)
        bs_annual, pnl_annual, cf_annual = t.calculate_kpis(bs_annual, pnl_annual, cf_annual)
        pnl_annual_prev, bs_annual_prev, cf_annual_prev = t.create_previous_year_dataframes(bs_annual, pnl_annual, cf_annual)
        pnl_concat, bs_concat, cf_concat = t.concatenate_dataframes(bs_annual, pnl_annual, cf_annual, bs_annual_prev, pnl_annual_prev, cf_annual_prev)
        pnl_concat, bs_concat, cf_concat = t.generate_insights(pnl_concat, bs_concat, cf_concat)

        # Ensure insights columns are strings to avoid serialization issues
        pnl_concat['insights_prev'] = pnl_concat['insights_prev'].astype(str)
        bs_concat['insights_prev'] = bs_concat['insights_prev'].astype(str)
        cf_concat['insights_prev'] = cf_concat['insights_prev'].astype(str)

        # Store the data in session state
        st.session_state['pnl_concat'] = pnl_concat
        st.session_state['bs_concat'] = bs_concat
        st.session_state['cf_concat'] = cf_concat
        st.session_state['financial_data_loaded'] = True
        st.session_state['insights_generated'] = False

        st.success("🎉 Financial data successfully loaded! Navigate through the tabs to explore more.")

    except Exception as e:
        st.error(f"An error occurred while retrieving or processing the data: {e}")

# Create Tabs to Organize the Analysis
tabs = st.tabs(["🏠 Overview", "📜 Balance Sheet", "💸 Profit & Loss", "💰 Cash Flow", "📊 Trends & Comparisons"])

# Overview Tab
with tabs[0]:
    st.header("🏠 Overview")
    
    if st.session_state['financial_data_loaded']:
        # Display key metrics using metric cards
        if 'totalAssets' in st.session_state['bs_concat'].columns:
            total_assets = st.session_state['bs_concat']['totalAssets'].iloc[-1]
            st.metric(label="Total Assets", value=f"${total_assets:,.2f}")
        else:
            st.warning("Total Assets data is not available.")

        if 'netIncome' in st.session_state['pnl_concat'].columns:
            net_income = st.session_state['pnl_concat']['netIncome'].iloc[-1]
            st.metric(label="Net Income", value=f"${net_income:,.2f}")
        else:
            st.warning("Net Income data is not available.")
        
        if 'operatingCashflow' in st.session_state['cf_concat'].columns:
            operating_cash_flow = st.session_state['cf_concat']['operatingCashflow'].iloc[-1]
            st.metric(label="Operating Cash Flow", value=f"${operating_cash_flow:,.2f}")
        else:
            st.warning("Operating Cash Flow data is not available.")

        # Plotly Line Chart for Revenue Growth
        if 'totalRevenue' in st.session_state['pnl_concat'].columns:
            st.subheader("📈 Revenue Growth Over Time")
            filtered_data = st.session_state['pnl_concat']
            fig = px.line(filtered_data, x='fiscalDateEnding', y='totalRevenue', title='Total Revenue Over Time')
            st.plotly_chart(fig)
        else:
            st.warning("Total Revenue data is not available for plotting.")

# Balance Sheet Tab
with tabs[1]:
    st.header("📜 Balance Sheet Analysis")
    if st.session_state['financial_data_loaded']:
        st.write("Below is the balance sheet overview:")
        st.dataframe(st.session_state['bs_concat'])

        # Dropdown for Year Selection within the Balance Sheet Tab
        available_years = st.session_state['bs_concat']['fiscalDateEnding'].unique()
        selected_year_bs = st.selectbox("📅 Select a Year to View Balance Sheet Insights:", available_years, key="year_select_bs")

        # Plotly Bar Chart for Total Assets vs. Total Liabilities
        filtered_data = st.session_state['bs_concat'][st.session_state['bs_concat']['fiscalDateEnding'] == selected_year_bs]
        fig = px.bar(filtered_data, x='fiscalDateEnding', y=['totalAssets', 'totalLiabilities'], barmode='group', title='Total Assets vs. Total Liabilities')
        st.plotly_chart(fig)

# Profit & Loss Tab
with tabs[2]:
    st.header("💸 Profit & Loss Statement Analysis")
    if st.session_state['financial_data_loaded']:
        st.write("Below is the profit and loss statement overview:")
        st.dataframe(st.session_state['pnl_concat'])

        # Dropdown for Year Selection within the Profit & Loss Tab
        available_years = st.session_state['pnl_concat']['fiscalDateEnding'].unique()
        selected_year_pnl = st.selectbox("📅 Select a Year to View P&L Insights:", available_years, key="year_select_pnl")

        # Plotly Stacked Bar Chart for Revenue vs. Expenses
        filtered_data = st.session_state['pnl_concat'][st.session_state['pnl_concat']['fiscalDateEnding'] == selected_year_pnl]
        fig = px.bar(filtered_data, x='fiscalDateEnding', y=['totalRevenue', 'operatingExpenses'], barmode='stack', title='Revenue vs. Operating Expenses')
        st.plotly_chart(fig)

# Cash Flow Tab
with tabs[3]:
    st.header("💰 Cash Flow Analysis")
    if st.session_state['financial_data_loaded']:
        st.write("Below is the cash flow statement overview:")
        st.dataframe(st.session_state['cf_concat'])

        # Dropdown for Year Selection within the Cash Flow Tab
        available_years = st.session_state['cf_concat']['fiscalDateEnding'].unique()
        selected_year_cf = st.selectbox("📅 Select a Year to View Cash Flow Insights:", available_years, key="year_select_cf")

        # Plotly Line Chart for Operating, Investing, and Financing Cash Flows
        filtered_data = st.session_state['cf_concat'][st.session_state['cf_concat']['fiscalDateEnding'] == selected_year_cf]
        fig = px.line(filtered_data, x='fiscalDateEnding', y=['operatingCashflow', 'investingCashFlow', 'financingCashFlow'], title='Cash Flow Activities Over Time')
        st.plotly_chart(fig)


# Trends & Comparisons Tab
with tabs[4]:
    st.header("📊 Trends and Comparisons")
    if st.session_state['financial_data_loaded']:
        # Dropdown for Year Selection
        available_years = st.session_state['bs_concat']['fiscalDateEnding'].unique()
        selected_year = st.selectbox("📅 Select a Year to View Insights:", available_years, key="year_select_trends")

        # Multi-Metric Comparison Line Chart
        st.subheader("Multi-Year Comparison of Key Metrics")
        filtered_data = st.session_state['bs_concat'][st.session_state['bs_concat']['fiscalDateEnding'].isin(available_years)]
        fig = px.line(filtered_data, x='fiscalDateEnding', y=['totalAssets', 'totalLiabilities', 'equity'], title='Multi-Year Comparison of Total Assets, Liabilities, and Equity')
        st.plotly_chart(fig)

        # Scatter Plot for Correlation Analysis (e.g., Net Income vs Operating Cash Flow)
        st.subheader("Correlation Analysis: Net Income vs Operating Cash Flow")
        pnl_data = st.session_state['pnl_concat']
        cf_data = st.session_state['cf_concat']
        merged_data = pd.merge(pnl_data, cf_data, on='fiscalDateEnding', suffixes=('_pnl', '_cf'))
        fig_scatter = px.scatter(merged_data, x='netIncome', y='operatingCashflow', title='Net Income vs Operating Cash Flow')
        st.plotly_chart(fig_scatter)

# Footer with Contact Information
st.markdown(
    "<hr><p style='text-align:center; color:grey;'>Automated Financial Analysis Tool © 2024. Developed by [Your Name]</p>",
    unsafe_allow_html=True
)
