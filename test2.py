import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import functions as py  # Import the functions module
import transform as t

# Set Streamlit page configuration
st.set_page_config(page_title="Automated Financial Report Analysis Tool", page_icon="📊", layout="wide")

# Sidebar with helpful links and filters
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
if 'selected_year_range' not in st.session_state:
    st.session_state['selected_year_range'] = None
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

# Display the Year Range Slider if Financial Data is Loaded
if st.session_state['financial_data_loaded']:
    st.header("📅 Select Year Range to Analyze")
    available_years = st.session_state['bs_concat']['fiscalDateEnding'].unique()
    start_year, end_year = st.slider(
        "Select Year Range",
        min_value=int(available_years.min()),
        max_value=int(available_years.max()),
        value=(int(available_years.min()), int(available_years.max()))
    )
    
    # Store selected year range in session state
    st.session_state['selected_year_range'] = (start_year, end_year)

    # Extract data for the selected year range
    filtered_bs_data = st.session_state['bs_concat'][
        (st.session_state['bs_concat']['fiscalDateEnding'].astype(int) >= start_year) & 
        (st.session_state['bs_concat']['fiscalDateEnding'].astype(int) <= end_year)
    ]
    filtered_pnl_data = st.session_state['pnl_concat'][
        (st.session_state['pnl_concat']['fiscalDateEnding'].astype(int) >= start_year) & 
        (st.session_state['pnl_concat']['fiscalDateEnding'].astype(int) <= end_year)
    ]
    filtered_cf_data = st.session_state['cf_concat'][
        (st.session_state['cf_concat']['fiscalDateEnding'].astype(int) >= start_year) & 
        (st.session_state['cf_concat']['fiscalDateEnding'].astype(int) <= end_year)
    ]

# Display Tabs for Financial Statements
if st.session_state['financial_data_loaded']:
    tabs = st.tabs(["Overview", "Balance Sheet", "Profit & Loss", "Cash Flow", "Key Metrics Dashboard", "Correlation Analysis"])

    # Overview Tab
    with tabs[0]:
        st.header("📊 Overview of Financial Metrics")
        if not filtered_bs_data.empty and not filtered_pnl_data.empty and not filtered_cf_data.empty:
            st.metric(label="Total Assets", value=f"${filtered_bs_data['totalAssets'].iloc[-1]:,.2f}")
            st.metric(label="Net Income", value=f"${filtered_pnl_data['netIncome'].iloc[-1]:,.2f}")
            st.metric(label="Operating Cash Flow", value=f"${filtered_cf_data['operatingCashflow'].iloc[-1]:,.2f}")
        else:
            st.warning("Not all financial data is available for the selected year range.")

    # Balance Sheet Tab
    with tabs[1]:
        st.header("📄 Balance Sheet Data")
        st.dataframe(data=filtered_bs_data)

        # Plot Total Assets over time
        fig_assets = px.line(filtered_bs_data, x='fiscalDateEnding', y='totalAssets', title='Total Assets Over Time')
        st.plotly_chart(fig_assets)

        # Plot Debt to Equity Ratio over time
        fig_debt_equity = px.line(filtered_bs_data, x='fiscalDateEnding', y='debtToEquityRatio', title='Debt to Equity Ratio Over Time')
        st.plotly_chart(fig_debt_equity)

        # Generate Insights for Balance Sheet
        if st.button("💡 Generate Balance Sheet Insights", key="bs_insights_button"):
            st.session_state['bs_insights_generated'] = True

        # Display insights if generated
        if st.session_state['bs_insights_generated']:
            st.subheader("🧾 Balance Sheet Insights")
            insights = filtered_bs_data[['fiscalDateEnding', 'insights']].dropna()
            for _, row in insights.iterrows():
                st.markdown(f"**{row['fiscalDateEnding']} Insights**: {row['insights']}")

    # Profit & Loss Tab
    with tabs[2]:
        st.header("📄 Profit and Loss Statement Data")
        st.dataframe(data=filtered_pnl_data)

        # Plot Net Income over time
        fig_net_income = px.line(filtered_pnl_data, x='fiscalDateEnding', y='netIncome', title='Net Income Over Time')
        st.plotly_chart(fig_net_income)

        # Plot Gross Margin over time
        fig_gross_margin = px.line(filtered_pnl_data, x='fiscalDateEnding', y='grossMargin', title='Gross Margin Over Time')
        st.plotly_chart(fig_gross_margin)

        # Generate Insights for Profit & Loss
        if st.button("💡 Generate P&L Insights", key="pnl_insights_button"):
            st.session_state['pnl_insights_generated'] = True

        # Display insights if generated
        if st.session_state['pnl_insights_generated']:
            st.subheader("💸 Profit and Loss Insights")
            insights = filtered_pnl_data[['fiscalDateEnding', 'insights']].dropna()
            for _, row in insights.iterrows():
                st.markdown(f"**{row['fiscalDateEnding']} Insights**: {row['insights']}")

    # Cash Flow Tab
    with tabs[3]:
        st.header("📄 Cash Flow Data")
        st.dataframe(data=filtered_cf_data)

        # Plot Operating Cash Flow over time
        fig_operating_cf = px.line(filtered_cf_data, x='fiscalDateEnding', y='operatingCashflow', title='Operating Cash Flow Over Time')
        st.plotly_chart(fig_operating_cf)

        # Generate Insights for Cash Flow
        if st.button("💡 Generate Cash Flow Insights", key="cf_insights_button"):
            st.session_state['cf_insights_generated'] = True

        # Display insights if generated
        if st.session_state['cf_insights_generated']:
            st.subheader("💰 Cash Flow Insights")
            insights = filtered_cf_data[['fiscalDateEnding', 'insights']].dropna()
            for _, row in insights.iterrows():
                st.markdown(f"**{row['fiscalDateEnding']} Insights**: {row['insights']}")

    # Key Metrics Dashboard
    with tabs[4]:
        st.header("📊 Key Metrics Dashboard")
        selected_metrics = st.multiselect(
            "Select Metrics to Visualize", 
            options=filtered_bs_data.columns, 
            default=["totalAssets", "totalLiabilities"]
        )
        if selected_metrics:
            fig_custom_metrics = px.line(
                filtered_bs_data, 
                x='fiscalDateEnding', 
                y=selected_metrics, 
                title='Selected Metrics Over Time'
            )
            st.plotly_chart(fig_custom_metrics)

    # Correlation Analysis Tab
    with tabs[5]:
        st.header("🔗 Correlation Analysis")
        corr_data = filtered_bs_data[['totalAssets', 'totalLiabilities', 'debtToEquityRatio', 'workingCapital']].dropna()
        corr_matrix = corr_data.corr()

        # Display Correlation Heatmap
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
