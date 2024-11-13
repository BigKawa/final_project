import streamlit as st
import pandas as pd
import numpy as np
import functions as py  # Import the functions module
import transform as t

# Streamlit App
st.title("📊 Automated Financial Report Analysis Tool")
st.caption("Analyze the financial report of a company using Streamlit and Python.")

# User Input Section
st.header("Company Financial Data Analysis")
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
if st.button("Get Financial Data"):
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

    except Exception as e:
        st.error(f"An error occurred while retrieving or processing the data: {e}")

# Display the data if loaded
if st.session_state['financial_data_loaded']:
    st.header("Balance Sheet Data")
    st.dataframe(data=st.session_state['bs_concat'])

    st.header("Profit and Loss Statement Data")
    st.dataframe(data=st.session_state['pnl_concat'])

    st.header("Cash Flow Data")
    st.dataframe(data=st.session_state['cf_concat'])

    # Dropdown for Year Selection
    available_years = st.session_state['bs_concat']['fiscalDateEnding'].unique()
    selected_year = st.selectbox("Select a Year to View Insights:", available_years, key="year_select")

    # Store selected year in session state
    st.session_state['selected_year'] = selected_year

    # Button to generate insights for the selected year
    if st.button("Generate Insights for Selected Year"):
        # Display Yearly Insights for Selected Year
        st.session_state['insights_generated'] = True

# Display Insights if Generated
if st.session_state['insights_generated'] and st.session_state['selected_year']:
    st.subheader(f"**Insights for the Year {st.session_state['selected_year']}**")

    # Filtering data for the selected year
    bs_year_data = st.session_state['bs_concat'][st.session_state['bs_concat']['fiscalDateEnding'] == st.session_state['selected_year']]
    pnl_year_data = st.session_state['pnl_concat'][st.session_state['pnl_concat']['fiscalDateEnding'] == st.session_state['selected_year']]
    cf_year_data = st.session_state['cf_concat'][st.session_state['cf_concat']['fiscalDateEnding'] == st.session_state['selected_year']]


    # Displaying Balance Sheet Insights
    if not bs_year_data.empty:
        st.subheader("Balance Sheet Insights") 
        
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

    # Displaying Profit and Loss Insights
    if not pnl_year_data.empty:
        st.subheader("Profit and Loss Insights") 
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

    # Displaying Cash Flow Insights
    if not cf_year_data.empty:
        st.subheader("Cashflow Insights") 
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
