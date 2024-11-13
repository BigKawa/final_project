import streamlit as st
import pandas as pd
import numpy as np
import functions as py  # Import the functions module
import transform as t

# Set Streamlit page configuration (NEW)
st.set_page_config(page_title="Automated Financial Report Analysis Tool", page_icon="📊", layout="wide")

# Sidebar Content - Helpful Links and Contact Information (NEW)
st.sidebar.header("📚 Resources")
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
        # Ideally, replace this with the actual function to fetch data via an API call
        # Example: pnl_concat, bs_concat, cf_concat = t.transform_pipeline(company_symbol)

        # Testing with CSV data as placeholder for now
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
        st.session_state['insights_generated'] = False  # Reset insights status

        st.success("🎉 Financial data successfully loaded! Navigate through the tabs to explore more.")

    except Exception as e:
        st.error(f"An error occurred while retrieving or processing the data: {e}")

# Create Tabs to Organize the Analysis
tabs = st.tabs(["🏠 Overview", "🧾 Balance Sheet", "💸 Profit & Loss", "💰 Cash Flow", "📊 Trends & Comparisons"])

# Overview Tab
with tabs[0]:
    st.header("🏠 Overview")
    if st.session_state['financial_data_loaded']:
        st.write("Key KPIs and Metrics Overview")
        # Add a few key metrics for a quick overview
        total_assets = st.session_state['bs_concat']['totalAssets'].iloc[-1]
        total_liabilities = st.session_state['bs_concat']['totalLiabilities'].iloc[-1]
        net_income = st.session_state['pnl_concat']['netIncome'].iloc[-1]
        st.metric("Total Assets", f"${total_assets:,}")
        st.metric("Total Liabilities", f"${total_liabilities:,}")
        st.metric("Net Income", f"${net_income:,}")

# Balance Sheet Tab
with tabs[1]:
    st.header("🧾 Balance Sheet Analysis")
    if st.session_state['financial_data_loaded']:
        st.write("Below is the balance sheet overview:")
        st.dataframe(st.session_state['bs_concat'])
        # Add visualizations for balance sheet metrics here

# Profit & Loss Tab
with tabs[2]:
    st.header("💸 Profit & Loss Statement Analysis")
    if st.session_state['financial_data_loaded']:
        st.write("Below is the profit and loss statement overview:")
        st.dataframe(st.session_state['pnl_concat'])
        # Add visualizations for revenue, expenses, and profit

# Cash Flow Tab
with tabs[3]:
    st.header("💰 Cash Flow Analysis")
    if st.session_state['financial_data_loaded']:
        st.write("Below is the cash flow statement overview:")
        st.dataframe(st.session_state['cf_concat'])
        # Add visualizations for cash flows

# Trends & Comparisons Tab
with tabs[4]:
    st.header("📊 Trends and Comparisons")
    if st.session_state['financial_data_loaded']:
        # Dropdown for Year Selection
        available_years = st.session_state['bs_concat']['fiscalDateEnding'].unique()
        selected_year = st.selectbox("📅 Select a Year to View Insights:", available_years, key="year_select")

        # Store selected year in session state
        st.session_state['selected_year'] = selected_year

        # Button to generate insights for the selected year
        if st.button("💡 Generate Insights for Selected Year"):
            # Display Insights for the selected year
            st.session_state['insights_generated'] = True

        # Display Insights if Generated
        if st.session_state['insights_generated'] and st.session_state['selected_year']:
            st.subheader(f"**📊 Insights for the Year {st.session_state['selected_year']}**")
            # Displaying detailed insights for selected year
            # Add the existing insights code here

# Footer with Contact Information (NEW)
st.markdown(
    "<hr><p style='text-align:center; color:grey;'>Automated Financial Analysis Tool © 2024. Developed by [Your Name]</p>",
    unsafe_allow_html=True
)
