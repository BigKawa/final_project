import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import functions as py  # Import the functions module
import transform as t

# Set Streamlit page configuration
st.set_page_config(page_title="Automated Financial Report Analysis Tool", page_icon="📊", layout="wide")

# Sidebar with helpful links
st.sidebar.header("📚 Resources")
st.sidebar.markdown("[Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)")
st.sidebar.markdown("[Streamlit Documentation](https://docs.streamlit.io/)")

st.sidebar.header("📞 Contact Us")
st.sidebar.info("For any questions, feel free to reach out at [your.email@example.com](mailto:your.email@example.com)")

# Title and introduction
st.title("📊 Automated Financial Report Analysis Tool")
st.caption("Analyze the financial report of a company using Streamlit and Python.")

# User Input Section
st.header("🔍 Company Financial Data Analysis")
company_symbol = st.text_input("Enter Company Symbol:", value="MSFT")

# Initialize session states to store data and track insights
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
if 'bs_insights_generated' not in st.session_state:
    st.session_state['bs_insights_generated'] = False
if 'pnl_insights_generated' not in st.session_state:
    st.session_state['pnl_insights_generated'] = False
if 'cf_insights_generated' not in st.session_state:
    st.session_state['cf_insights_generated'] = False

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

# Display Tabs for Financial Statements
if st.session_state['financial_data_loaded']:
    tabs = st.tabs(["Overview", "Balance Sheet", "Profit & Loss", "Cash Flow"])

    # Overview Tab
    with tabs[0]:
        st.header("📊 Overview of Financial Metrics")

        # Dropdown for Year Selection
        available_years = st.session_state['bs_concat']['fiscalDateEnding'].unique()
        selected_year = st.selectbox("📅 Select a Year to View Insights:", available_years, key="year_select")

        # Store selected year in session state
        st.session_state['selected_year'] = selected_year

        # Summary metrics for quick view
        st.subheader(f"**Financial Summary for {selected_year}**")

        # Extract relevant data for the selected year
        bs_data = st.session_state['bs_concat'][st.session_state['bs_concat']['fiscalDateEnding'] == selected_year]
        pnl_data = st.session_state['pnl_concat'][st.session_state['pnl_concat']['fiscalDateEnding'] == selected_year]
        cf_data = st.session_state['cf_concat'][st.session_state['cf_concat']['fiscalDateEnding'] == selected_year]

        # Display key metrics
        if not bs_data.empty and not pnl_data.empty and not cf_data.empty:
            st.metric(label="Total Assets", value=f"${bs_data['totalAssets'].values[0]:,.2f}")
            st.metric(label="Net Income", value=f"${pnl_data['netIncome'].values[0]:,.2f}")
            st.metric(label="Operating Cash Flow", value=f"${cf_data['operatingCashflow'].values[0]:,.2f}")
        else:
            st.warning("Not all financial data is available for the selected year.")

    # Balance Sheet Tab
    with tabs[1]:
        st.header("📄 Balance Sheet Data")
        st.dataframe(data=st.session_state['bs_concat'])

        # Plot Total Assets over time
        fig_assets = px.line(st.session_state['bs_concat'], x='fiscalDateEnding', y='totalAssets', title='Total Assets Over Time')
        st.plotly_chart(fig_assets)

        # Button to generate insights for the selected year in Balance Sheet
        if st.button("💡 Generate Balance Sheet Insights for Selected Year", key="bs_insights_button"):
            st.session_state['bs_insights_generated'] = True

        # Display insights if generated
        if st.session_state['bs_insights_generated']:
            # Filtering data for the selected year
            bs_year_data = st.session_state['bs_concat'][st.session_state['bs_concat']['fiscalDateEnding'] == st.session_state['selected_year']]
            if not bs_year_data.empty:
                st.subheader("🧾 Balance Sheet Insights")
                if 'insights' in bs_year_data.columns:
                    st.markdown(f"**Balance Sheet Insights**: {bs_year_data['insights'].values[0]}")
                if 'previous_year_insights' in bs_year_data.columns:
                    st.markdown(f"**Previous Year Insights**: {bs_year_data['previous_year_insights'].values[0]}")
                if 'year_comparison_insight' in bs_year_data.columns:
                    st.markdown(f"**Year Comparison Insight**: {bs_year_data['year_comparison_insight'].values[0]}")
                if 'patterns' in bs_year_data.columns:
                    st.markdown(f"**Patterns**: {bs_year_data['patterns'].values[0]}")
            else:
                st.warning("No insights available for the Balance Sheet for the selected year.")

    # Profit & Loss Tab
    with tabs[2]:
        st.header("📄 Profit and Loss Statement Data")
        st.dataframe(data=st.session_state['pnl_concat'])

        # Plot Net Income over time
        fig_net_income = px.line(st.session_state['pnl_concat'], x='fiscalDateEnding', y='netIncome', title='Net Income Over Time')
        st.plotly_chart(fig_net_income)

        # Button to generate insights for the selected year in P&L
        if st.button("💡 Generate P&L Insights for Selected Year", key="pnl_insights_button"):
            st.session_state['pnl_insights_generated'] = True

        # Display insights if generated
        if st.session_state['pnl_insights_generated']:
            # Filtering data for the selected year
            pnl_year_data = st.session_state['pnl_concat'][st.session_state['pnl_concat']['fiscalDateEnding'] == st.session_state['selected_year']]
            if not pnl_year_data.empty:
                st.subheader("💸 Profit and Loss Insights")
                if 'insights' in pnl_year_data.columns:
                    st.markdown(f"**Profit and Loss Current Insights**: {pnl_year_data['insights'].values[0]}")
                if 'previous_year_insights' in pnl_year_data.columns:
                    st.markdown(f"**Previous Year Insights**: {pnl_year_data['previous_year_insights'].values[0]}")
                if 'year_comparison_insight' in pnl_year_data.columns:
                    st.markdown(f"**Year Comparison Insight**: {pnl_year_data['year_comparison_insight'].values[0]}")
                if 'patterns' in pnl_year_data.columns:
                    st.markdown(f"**Patterns**: {pnl_year_data['patterns'].values[0]}")
            else:
                st.warning("No insights available for the Profit and Loss Statement for the selected year.")

    # Cash Flow Tab
    with tabs[3]:
        st.header("📄 Cash Flow Data")
        st.dataframe(data=st.session_state['cf_concat'])

        # Plot Operating Cash Flow over time
        fig_operating_cf = px.line(st.session_state['cf_concat'], x='fiscalDateEnding', y='operatingCashflow', title='Operating Cash Flow Over Time')
        st.plotly_chart(fig_operating_cf)

        # Button to generate insights for the selected year in Cash Flow
        if st.button("💡 Generate Cash Flow Insights for Selected Year", key="cf_insights_button"):
            st.session_state['cf_insights_generated'] = True

        # Display insights if generated
        if st.session_state['cf_insights_generated']:
            # Filtering data for the selected year
            cf_year_data = st.session_state['cf_concat'][st.session_state['cf_concat']['fiscalDateEnding'] == st.session_state['selected_year']]
            if not cf_year_data.empty:
                st.subheader("💰 Cash Flow Insights")
                if 'insights' in cf_year_data.columns:
                    st.markdown(f"**Cash Flow Current Insights**: {cf_year_data['insights'].values[0]}")
                if 'previous_year_insights' in cf_year_data.columns:
                    st.markdown(f"**Previous Year Insights**: {cf_year_data['previous_year_insights'].values[0]}")
                if 'year_comparison_insight' in cf_year_data.columns:
                    st.markdown(f"**Year Comparison Insight**: {cf_year_data['year_comparison_insight'].values[0]}")
                if 'patterns' in cf_year_data.columns:
                    st.markdown(f"**Patterns**: {cf_year_data['patterns'].values[0]}")
            else:
                st.warning("No insights available for the Cash Flow Statement for the selected year.")

# Footer with Contact Information (NEW)
st.markdown(
    "<hr><p style='text-align:center; color:grey;'>Automated Financial Analysis Tool © 2024. Developed by [Your Name]</p>",
    unsafe_allow_html=True
)
