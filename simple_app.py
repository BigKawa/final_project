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
company_symbol = st.text_input("Enter Company Symbol:", value="MSFT").upper()

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
        
        # Load the Data from AlphaVantage API
        bs_concat, cf_concat, pnl_concat = t.transform_pipeline(company_symbol)
        
     
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

# Display Year Selection for Generating Insights Only
if st.session_state['financial_data_loaded']:
    st.header("📅 Select Year for Generating Insights")
    available_years = st.session_state['bs_concat']['fiscalDateEnding'].unique()
    selected_year = st.selectbox("Select Year for Insights", available_years)
    
    # Store selected year in session state for insights generation only
    st.session_state['selected_year'] = selected_year

    # Filter data for the selected year (for insights only)
    bs_year_data = st.session_state['bs_concat'][st.session_state['bs_concat']['fiscalDateEnding'] == st.session_state['selected_year']]
    pnl_year_data = st.session_state['pnl_concat'][st.session_state['pnl_concat']['fiscalDateEnding'] == st.session_state['selected_year']]
    cf_year_data = st.session_state['cf_concat'][st.session_state['cf_concat']['fiscalDateEnding'] == st.session_state['selected_year']]

# Display Year Range Slider for Plot Visualizations
if st.session_state['financial_data_loaded']:
    st.header("📊 Select Year Range to Visualize Trends")
    start_year, end_year = st.slider(
        "Select Year Range",
        min_value=int(available_years.min()),
        max_value=int(available_years.max()),
        value=(int(available_years.min()), int(available_years.max()))
    )

    # Filter data based on selected year range for plotting (for visualizations)
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

# Display Tabs for Financial Statements and Insights
if st.session_state['financial_data_loaded']:
    tabs = st.tabs(["Overview", "Balance Sheet", "Profit & Loss", "Cash Flow", "Key Metrics Dashboard", "Correlation Analysis"])

    # Overview Tab
    with tabs[0]:
        st.header("📊 Overview of Financial Metrics")
        if not filtered_bs_data.empty and not filtered_pnl_data.empty and not filtered_cf_data.empty:
            latest_year = filtered_bs_data['fiscalDateEnding'].iloc[0]
            st.metric(label=f"Total Assets (as of {latest_year})", value=f"${filtered_bs_data['totalAssets'].iloc[0]:,.2f}")
            st.metric(label="Net Income", value=f"${filtered_pnl_data['netIncome'].iloc[0]:,.2f}")
            st.metric(label="Operating Cash Flow", value=f"${filtered_cf_data['operatingCashflow'].iloc[0]:,.2f}")
            
            # Plotting total assets over selected year range
            fig_assets = px.line(filtered_bs_data, x='fiscalDateEnding', y='totalAssets', title='Total Assets Over Time')
            st.plotly_chart(fig_assets)

            # Plotting net income over selected year range
            fig_net_income = px.line(filtered_pnl_data, x='fiscalDateEnding', y='netIncome', title='Net Income Over Time')
            st.plotly_chart(fig_net_income)
        else:
            st.warning("Not all financial data is available.")

    # Balance Sheet Tab
    with tabs[1]:
        st.header("📄 Balance Sheet Data")
        st.dataframe(data=filtered_bs_data)

        # Plotting Asset Breakdown (stacked bar chart)
        fig_asset_breakdown = px.bar(
            filtered_bs_data,
            x='fiscalDateEnding',
            y=['totalCurrentAssets', 'totalNonCurrentAssets', 'cashAndShortTermInvestments', 'inventory'],
            title='Asset Breakdown Over Time',
            barmode='stack'
        )
        st.plotly_chart(fig_asset_breakdown)

        # Plotting Total Assets vs. Total Liabilities over selected year range
        fig_total_assets_vs_liabilities = px.line(
            filtered_bs_data, 
            x='fiscalDateEnding', 
            y=['totalAssets', 'totalLiabilities'], 
            title='Total Assets vs. Total Liabilities Over Time'
        )
        st.plotly_chart(fig_total_assets_vs_liabilities)

        # Plotting Debt Composition (current vs. non-current liabilities)
        fig_debt_composition = px.bar(
            filtered_bs_data,
            x='fiscalDateEnding',
            y=['totalCurrentLiabilities', 'totalNonCurrentLiabilities'],
            title='Debt Composition Over Time (Current vs. Non-Current Liabilities)',
            barmode='stack'
        )
        st.plotly_chart(fig_debt_composition)

        # Plotting Shareholder Equity vs. Debt-to-Equity Ratio
        fig_equity_vs_debt_ratio = px.line(
            filtered_bs_data,
            x='fiscalDateEnding',
            y=['totalShareholderEquity', 'debtToEquityRatio'],
            title='Shareholder Equity vs. Debt-to-Equity Ratio Over Time'
        )
        st.plotly_chart(fig_equity_vs_debt_ratio)

        # Generate Insights for Balance Sheet
        if st.button("💡 Generate Balance Sheet Insights", key="bs_insights_button"):
            st.session_state['bs_insights_generated'] = True

        # Displaying Balance Sheet Insights if generated
        if st.session_state['bs_insights_generated'] and not bs_year_data.empty:
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
        st.dataframe(data=filtered_pnl_data)

        # Plotting Revenue vs. Operating Expenses over selected year range
        fig_revenue_vs_expenses = px.line(
            filtered_pnl_data,
            x='fiscalDateEnding',
            y=['totalRevenue', 'operatingExpenses'],
            title='Revenue vs. Operating Expenses Over Time'
        )
        st.plotly_chart(fig_revenue_vs_expenses)

        # Plotting Operating Income vs. Net Income over selected year range
        fig_operating_vs_net_income = px.line(
            filtered_pnl_data,
            x='fiscalDateEnding',
            y=['operatingIncome', 'netIncome'],
            title='Operating Income vs. Net Income Over Time'
        )
        st.plotly_chart(fig_operating_vs_net_income)

        # Plotting Cost of Goods Sold vs. Total Revenue
        fig_cogs_vs_revenue = px.line(
            filtered_pnl_data,
            x='fiscalDateEnding',
            y=['totalRevenue', 'costOfRevenue'],
            title='Cost of Goods Sold vs. Total Revenue Over Time'
        )
        st.plotly_chart(fig_cogs_vs_revenue)

        # Plotting R&D and SG&A Expenses
        fig_rd_vs_sga = px.bar(
            filtered_pnl_data,
            x='fiscalDateEnding',
            y=['researchAndDevelopment', 'sellingGeneralAndAdministrative'],
            title='R&D vs. SG&A Expenses Over Time',
            barmode='stack'
        )
        st.plotly_chart(fig_rd_vs_sga)

        # Generate Insights for Profit & Loss
        if st.button("💡 Generate P&L Insights", key="pnl_insights_button"):
            st.session_state['pnl_insights_generated'] = True

        # Displaying Profit and Loss Insights if generated
        if st.session_state['pnl_insights_generated'] and not pnl_year_data.empty:
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
        st.dataframe(data=filtered_cf_data)

        # Plotting Cash Flow from Operating, Investing, and Financing Activities (stacked bar chart)
        fig_cash_flow_activities = px.bar(
            filtered_cf_data,
            x='fiscalDateEnding',
            y=['operatingCashflow', 'cashflowFromInvestment', 'cashflowFromFinancing'],
            title='Cash Flow from Operating, Investing, and Financing Activities',
            barmode='stack'
        )
        st.plotly_chart(fig_cash_flow_activities)

        # Plotting Free Cash Flow over selected year range (if available)
        if 'freeCashFlow' in filtered_cf_data.columns:
            fig_free_cashflow = px.line(filtered_cf_data, x='fiscalDateEnding', y='freeCashFlow', title='Free Cash Flow Over Time')
            st.plotly_chart(fig_free_cashflow)

        # Generate Insights for Cash Flow
        if st.button("💡 Generate Cash Flow Insights", key="cf_insights_button"):
            st.session_state['cf_insights_generated'] = True

        # Displaying Cash Flow Insights if generated
        if st.session_state['cf_insights_generated'] and not cf_year_data.empty:
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

    # Key Metrics Dashboard Tab (Tab 4)
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

    # Correlation Analysis Tab (Tab 5)
    with tabs[5]:
        st.header("🔗 Correlation Analysis")
        
        # Prepare Data for Correlation
        corr_data = pd.concat([
            filtered_bs_data[['totalAssets', 'totalLiabilities', 'debtToEquityRatio']],
            filtered_pnl_data[['netIncome', 'grossMargin', 'operatingMargin']],
            filtered_cf_data[['operatingCashflow']]
        ], axis=1).dropna()
        
        # Correlation Heatmap
        corr_matrix = corr_data.corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

        # Scatter Plot Matrix of Key Metrics
        fig_scatter_matrix = px.scatter_matrix(corr_data, dimensions=['totalAssets', 'totalLiabilities', 'debtToEquityRatio', 'netIncome', 'grossMargin'], title='Scatter Matrix of Key Metrics')
        st.plotly_chart(fig_scatter_matrix)

# Footer with Contact Information and Copyright
st.markdown(
    """
    <hr style="border:1px solid #ccc;">
    <div style="text-align:center; color:grey;">
        <p>Automated Financial Analysis Tool &copy; 2024. Developed by <a href="mailto:secret@secret.com">Linh Vuong</a></p>
        <p>For inquiries or secret, please contact <a href="mailto:secret@secret.com">secret@secret.com</a></p>
        <p><a href="htthttps://www.linkedin.com/in/linh-vuong/" target="_blank">Connect with us on LinkedIn</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
st.write(filtered_bs_data.columns)