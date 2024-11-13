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

        # Dropdown for Year Selection within the Balance Sheet Tab
        available_years = st.session_state['bs_concat']['fiscalDateEnding'].unique()
        selected_year_bs = st.selectbox("📅 Select a Year to View Balance Sheet Insights:", available_years, key="year_select_bs")

        # Button to generate insights for the selected year
        if st.button("💡 Generate Balance Sheet Insights"):
            with st.spinner('🔍 Generating Balance Sheet insights... Please wait while we analyze the data for you.'):
                # Filter the balance sheet data for the selected year
                bs_year_data = st.session_state['bs_concat'][st.session_state['bs_concat']['fiscalDateEnding'] == selected_year_bs]
                
                if not bs_year_data.empty:
                    st.subheader(f"**📊 Balance Sheet Insights for the Year {selected_year_bs}**")
                    if 'insights' in bs_year_data.columns:
                        st.markdown(f"**Balance Sheet Insights**: {bs_year_data['insights'].values[0]}")
                    if 'previous_year_insights' in bs_year_data.columns:
                        st.markdown(f"**Previous Year Insights**: {bs_year_data['previous_year_insights'].values[0]}")
                    if 'year_comparison_insight' in bs_year_data.columns:
                        st.markdown(f"**Year Comparison Insight**: {bs_year_data['year_comparison_insight'].values[0]}")
                    if 'patterns' in bs_year_data.columns:
                        st.markdown(f"**Patterns Identified**: {bs_year_data['patterns'].values[0]}")
                else:
                    st.warning("No insights available for the Balance Sheet for the selected year. Please try another year.")

# Profit & Loss Tab
with tabs[2]:
    st.header("💸 Profit & Loss Statement Analysis")
    if st.session_state['financial_data_loaded']:
        st.write("Below is the profit and loss statement overview:")
        st.dataframe(st.session_state['pnl_concat'])

        # Dropdown for Year Selection within the Profit & Loss Tab
        available_years = st.session_state['pnl_concat']['fiscalDateEnding'].unique()
        selected_year_pnl = st.selectbox("📅 Select a Year to View P&L Insights:", available_years, key="year_select_pnl")

        # Button to generate insights for the selected year
        if st.button("💡 Generate P&L Insights"):
            with st.spinner('🔍 Generating P&L insights... Please wait while we analyze the data for you.'):
                # Filter the P&L data for the selected year
                pnl_year_data = st.session_state['pnl_concat'][st.session_state['pnl_concat']['fiscalDateEnding'] == selected_year_pnl]
                
                if not pnl_year_data.empty:
                    st.subheader(f"**📊 Profit & Loss Insights for the Year {selected_year_pnl}**")
                    if 'insights' in pnl_year_data.columns:
                        st.markdown(f"**Profit & Loss Current Insights**: {pnl_year_data['insights'].values[0]}")
                    if 'previous_year_insights' in pnl_year_data.columns:
                        st.markdown(f"**Previous Year Insights**: {pnl_year_data['previous_year_insights'].values[0]}")
                    if 'year_comparison_insight' in pnl_year_data.columns:
                        st.markdown(f"**Year Comparison Insight**: {pnl_year_data['year_comparison_insight'].values[0]}")
                    if 'patterns' in pnl_year_data.columns:
                        st.markdown(f"**Patterns Identified**: {pnl_year_data['patterns'].values[0]}")
                else:
                    st.warning("No insights available for the Profit and Loss Statement for the selected year.")

# Cash Flow Tab
with tabs[3]:
    st.header("💰 Cash Flow Analysis")
    if st.session_state['financial_data_loaded']:
        st.write("Below is the cash flow statement overview:")
        st.dataframe(st.session_state['cf_concat'])

        # Dropdown for Year Selection within the Cash Flow Tab
        available_years = st.session_state['cf_concat']['fiscalDateEnding'].unique()
        selected_year_cf = st.selectbox("📅 Select a Year to View Cash Flow Insights:", available_years, key="year_select_cf")

        # Button to generate insights for the selected year
        if st.button("💡 Generate Cash Flow Insights"):
            with st.spinner('🔍 Generating Cash Flow insights... Please wait while we analyze the data for you.'):
                # Filter the cash flow data for the selected year
                cf_year_data = st.session_state['cf_concat'][st.session_state['cf_concat']['fiscalDateEnding'] == selected_year_cf]
                
                if not cf_year_data.empty:
                    st.subheader(f"**📊 Cash Flow Insights for the Year {selected_year_cf}**")
                    if 'insights' in cf_year_data.columns:
                        st.markdown(f"**Cash Flow Current Insights**: {cf_year_data['insights'].values[0]}")
                    if 'previous_year_insights' in cf_year_data.columns:
                        st.markdown(f"**Previous Year Insights**: {cf_year_data['previous_year_insights'].values[0]}")
                    if 'year_comparison_insight' in cf_year_data.columns:
                        st.markdown(f"**Year Comparison Insight**: {cf_year_data['year_comparison_insight'].values[0]}")
                    if 'patterns' in cf_year_data.columns:
                        st.markdown(f"**Patterns Identified**: {cf_year_data['patterns'].values[0]}")
                else:
                    st.warning("No insights available for the Cash Flow Statement for the selected year.")


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
