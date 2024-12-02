import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt  # Import the functions module
import transform as t
from variables import *



# Set Streamlit page configuration
st.set_page_config(page_title="Automated Financial Report Analysis Tool", page_icon="📊", layout="wide")

# Sidebar with helpful links and filters
st.sidebar.header("📚 Resources")
st.sidebar.markdown("[Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)")
st.sidebar.markdown("[Streamlit Documentation](https://docs.streamlit.io/)")
st.sidebar.markdown("Company List")
st.sidebar.markdown("[Download Link](https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo)")

st.sidebar.header("📞 Contact Us")
st.sidebar.info("For any questions, feel free to reach out at [linh.vuong@web.de](mailto:linh.vuong@web.de)")

# Sidebar Header for KPI Definitions
st.sidebar.header("📊 KPI Definitions")

# Adding improved styling for definitions to make them look more attractive
def styled_markdown(name, definition, name_color="#FFD700", definition_color="#FFFFFF", background_color="#222222"):
    return f'<p style="background-color:{background_color}; padding:6px; border-radius:6px; font-family:Arial, sans-serif;">' \
           f'<strong style="color:{name_color}; font-size:16px;">{name}:</strong> ' \
           f'<span style="color:{definition_color}; font-size:14px;">{definition}</span>' \
           f'</p>'

# Define Colors for Different KPI Groups
profit_loss_color = "#1E90FF"  # Dodger blue
cash_flow_color = "#32CD32"     # Lime green
balance_sheet_color = "#FF4500" # Orange red

# Create Expandable Sections for KPI Groups, with all KPIs and their definitions inside
with st.sidebar.expander("🏦 Balance Sheet KPIs", expanded=False):
    for kpi in balance_sheet_kpis:
        definition = kpi_definitions.get(kpi, "Definition not available")
        st.markdown(styled_markdown(kpi.replace('_', ' ').title(), definition, name_color="#FFFFFF", background_color=balance_sheet_color), unsafe_allow_html=True)


with st.sidebar.expander("📈 Profit & Loss KPIs", expanded=False):
    for kpi in profit_loss_kpis:
        definition = kpi_definitions.get(kpi, "Definition not available")
        st.markdown(styled_markdown(kpi.replace('_', ' ').title(), definition, name_color="#FFFFFF", background_color=profit_loss_color), unsafe_allow_html=True)

with st.sidebar.expander("💸 Cash Flow KPIs", expanded=False):
    for kpi in cash_flow_kpis:
        definition = kpi_definitions.get(kpi, "Definition not available")
        st.markdown(styled_markdown(kpi.replace('_', ' ').title(), definition, name_color="#FFFFFF", background_color=cash_flow_color), unsafe_allow_html=True)


# Title and introduction
st.title("📊 Automated Financial Report Analysis Tool")
st.caption("Analyze the financial report of a company using Streamlit and Python.")

# User Input Section
st.header("🔍 Company Financial Data Analysis")
company_symbol = st.text_input("Enter Company Symbol:", value="MSFT").upper()

# Initialize session states to store data and track insights for coming Reruns
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

        # Store the data in session state between Reruns 
        st.session_state['pnl_concat'] = pnl_concat
        st.session_state['bs_concat'] = bs_concat
        st.session_state['cf_concat'] = cf_concat
        st.session_state['financial_data_loaded'] = True
        st.session_state['insights_generated'] = False

        st.success("🎉 Financial data successfully loaded! Navigate through the tabs to explore more.")

    except Exception as e:  # Errror Handling
        st.error(f"An error occurred while retrieving or processing the data: {e}") # Retrieve the Error using e as an argument

# Display Year Selection for Generating Insights Only
if st.session_state['financial_data_loaded']:
    st.header("📅 Select Year for Generating Insights")
    available_years = st.session_state['bs_concat']['fiscalDateEnding'].unique()  # get years 
    selected_year = st.selectbox("Select Year for Insights", available_years)  # put years in select box
    
    
    # Store selected year in session state for insights generation only
    st.session_state['selected_year'] = selected_year # save year in seperate session state / variable 

    # Filter data for the selected year (for insights only)
    # Example:
    # ['bs_concat']['fiscalDateEnding'] == st.session_state['selected_year']] is True for the selected year 
    # gets all rows in 'bs_concat' where 'fiscalDateEnding' is equal to the selected year
    bs_year_data = st.session_state['bs_concat'][st.session_state['bs_concat']['fiscalDateEnding'] == st.session_state['selected_year']]
    pnl_year_data = st.session_state['pnl_concat'][st.session_state['pnl_concat']['fiscalDateEnding'] == st.session_state['selected_year']]
    cf_year_data = st.session_state['cf_concat'][st.session_state['cf_concat']['fiscalDateEnding'] == st.session_state['selected_year']]

# Make sure financial data has been loaded and a year has been selected
if st.session_state['financial_data_loaded'] and st.session_state['selected_year']:
    st.header("🏥 Company Financial Health Score for Selected Year")
    st.markdown(
    """
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .animated-text {
        text-align: center;
        color: #1e90ff;
        font-size: 24px;
        text-shadow: 2px 2px 4px rgba(30, 144, 255, 0.4);
        animation: pulse 2s infinite;
    }
    </style>
    <div class="animated-text">🚧 Still a Work in Progress</div>
    """,
    unsafe_allow_html=True
)



    # Filter data for the selected year
    selected_year = st.session_state['selected_year']
    pnl_year_data = st.session_state['pnl_concat'][st.session_state['pnl_concat']['fiscalDateEnding'] == selected_year]
    bs_year_data = st.session_state['bs_concat'][st.session_state['bs_concat']['fiscalDateEnding'] == selected_year]
    cf_year_data = st.session_state['cf_concat'][st.session_state['cf_concat']['fiscalDateEnding'] == selected_year]

    # Ensure that the selected year data exists for all three financial statements
    if not pnl_year_data.empty and not bs_year_data.empty and not cf_year_data.empty:
        # Extract the single row for the selected year
        pnl_row = pnl_year_data.iloc[0]
        bs_row = bs_year_data.iloc[0]
        cf_row = cf_year_data.iloc[0]

        # Calculate health score based on the selected year's data
        health_score = t.calculate_health_score(pnl_row, bs_row, cf_row)

        # Determine label, color, and icon based on health score
        if health_score >= 85:
            label = "Excellent"
            color = "#28a745"  # Green
            icon = "🏆"
        elif 70 <= health_score < 85:
            label = "Good"
            color = "#17a2b8"  # Blue
            icon = "👍"
        elif 50 <= health_score < 70:
            label = "Average"
            color = "#ffc107"  # Yellow
            icon = "⚠️"
        else:
            label = "Poor"
            color = "#dc3545"  # Red
            icon = "❌"

        # Set colors based on health score ranges
        if health_score >= 80:
            color_gradient = "linear-gradient(135deg, #57B65F, #88D498)"  # Brightened green
            text_color = "#ffffff"  # White for readability
        elif health_score >= 60:
            color_gradient = "linear-gradient(135deg, #4E92E3, #83C1F4)"  # Brighter blue
            text_color = "#ffffff"  # White for readability
        elif health_score >= 40:
            color_gradient = "linear-gradient(135deg, #FFDD67, #FFE28D)"  # Softer yellow
            text_color = "#333333"  # Dark grey for good contrast
        elif health_score >= 20:
            color_gradient = "linear-gradient(135deg, #FF8E42, #FFB876)"  # Slightly softer orange
            text_color = "#ffffff"  # White for readability
        else:
            color_gradient = "linear-gradient(135deg, #F26D6D, #FF9999)"  # Softer red/pink
            text_color = "#ffffff"  # White for readability

                    
                
                

        st.markdown(
            f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');

            .animated-container {{
                background: {color_gradient};  /* Dynamic Gradient */
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                font-family: 'Poppins', sans-serif;  /* Modern Font */
                transition: transform 0.3s ease-in-out;  /* Smooth transition for hover effect */
            }}

            .animated-container:hover {{
                transform: scale(1.05);  /* Slightly increase size on hover */
            }}

            .animated-title {{
                color: {text_color};  /* Dynamic Text Color for Better Contrast */
                font-size: 28px;
                font-weight: bold;
                text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
            }}
            </style>

            <div class="animated-container">
                <h2 class="animated-title">{icon} Financial Health Score: {health_score} ({label})</h2>
            </div>
            """,
            unsafe_allow_html=True
        )



        # Display the health score as a progress bar (like a battery)
        st.progress(health_score / 100)

        # Provide additional tips based on the health score
        if health_score >= 85:
            st.success("The company is in excellent financial health. This Company is doing well!")
        elif 70 <= health_score < 85:
            st.info("The company is in good financial health, but there may be opportunities for optimization.")
        elif 50 <= health_score < 70:
            st.warning("The company is in average financial health. This company may require strategies to improve key metrics.")
        else:
            st.error("The company's financial health is poor. Immediate action is recommended to improve stability for this company.")

    else:
        st.warning(f"Data for the year {selected_year} is incomplete or missing.")



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
    # Filtering between the sliders
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
    tabs = st.tabs(["Overview", "Balance Sheet", "Profit & Loss", "Cash Flow", "Key Metrics Dashboard", "Additional Analysis"])

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
            # Balance Sheet Insights
            if 'insights' in bs_year_data.columns:
                st.markdown(
                    '<p style="color:#32CD32; font-size:24px; background-color:#333333; padding:10px; border-radius:10px; text-align:center;"><strong>📊 Balance Sheet Current Insights</strong></p>',
                    unsafe_allow_html=True
                )
                st.markdown("<br>", unsafe_allow_html=True)  # Adds an empty line
                st.markdown(bs_year_data['insights'].values[0])

            # Previous Year Insights
            if 'previous_year_insights' in bs_year_data.columns:
                st.markdown(
                    '<p style="color:#FFA500; font-size:22px; background-color:#444444; padding:8px; border-radius:8px; text-align:center;"><strong>📅 Previous Year Insights</strong></p>',
                    unsafe_allow_html=True
                )
                st.markdown("<br>", unsafe_allow_html=True)  # Adds an empty line
                st.markdown(bs_year_data['previous_year_insights'].values[0])

            # Year Comparison Insight
            if 'year_comparison_insight' in bs_year_data.columns:
                st.markdown(
                    '<p style="color:#00BFFF; font-size:20px; background-color:#333333; padding:6px; border-radius:8px; text-align:center;"><strong>🔄 Year Comparison Insight</strong></p>',
                    unsafe_allow_html=True
                )
                st.markdown("<br>", unsafe_allow_html=True)  # Adds an empty line
                st.markdown(bs_year_data['year_comparison_insight'].values[0])

            # Patterns
            if 'patterns' in bs_year_data.columns:
                st.markdown(
                    '<p style="color:#FFD700; font-size:18px; background-color:#444444; padding:4px; border-radius:8px; text-align:center;"><strong>🔍 Patterns</strong></p>',
                    unsafe_allow_html=True
                )
                st.markdown("<br>", unsafe_allow_html=True)  # Adds an empty line
                st.markdown(bs_year_data['patterns'].values[0])

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
            st.subheader("💸 Profit and Loss Insights:")
            if 'insights' in pnl_year_data.columns:
                st.markdown(
                    '<p style="color:#FFD700; font-size:24px; background-color:#333333; padding:10px; border-radius:10px; text-align:center;"><strong>💰 Profit and Loss Current Insights</strong></p>',
                    unsafe_allow_html=True
                )
                st.write("")  # Adds an empty line
                st.markdown(pnl_year_data['insights'].values[0])

            # Previous Year Insights - Adding 🕒 Emoji for time aspect of previous year
            if 'previous_year_insights' in pnl_year_data.columns:
                st.markdown(
    '<p style="color:#FFA500; font-size:22px; background-color:#444444; padding:8px; border-radius:8px; text-align:center;"><strong>📅 Previous Year Insights</strong></p>',
    unsafe_allow_html=True
)
                st.write("")  # Adds an empty line
                st.markdown(pnl_year_data['previous_year_insights'].values[0])

            # Year Comparison Insight - Adding 📊 Emoji for comparison
            if 'year_comparison_insight' in pnl_year_data.columns:
                st.markdown(
    '<p style="color:#00BFFF; font-size:20px; background-color:#333333; padding:6px; border-radius:8px; text-align:center;"><strong>🔄 Year Comparison Insight</strong></p>',
    unsafe_allow_html=True
)

                st.write("")  # Adds an empty line
                st.markdown(pnl_year_data['year_comparison_insight'].values[0])

            # Patterns - Adding 🔍 Emoji to indicate looking for patterns
            if 'patterns' in pnl_year_data.columns:
                st.markdown(
    '<p style="color:#FFD700; font-size:18px; background-color:#444444; padding:4px; border-radius:8px; text-align:center;"><strong>🔍 Patterns</strong></p>',
    unsafe_allow_html=True
)
                st.write("")  # Adds an empty line
                st.markdown(pnl_year_data['patterns'].values[0])

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
            # Cash Flow Current Insights
            if 'insights' in cf_year_data.columns:
                st.markdown(
    '<p style="color:#00FF00; font-size:24px; background-color:#333333; padding:10px; border-radius:10px; text-align:center;"><strong>💸 Cash Flow Current Insights</strong></p>',
    unsafe_allow_html=True
)

                st.markdown("<br>", unsafe_allow_html=True)  # Adds an empty line
                st.markdown(cf_year_data['insights'].values[0])

            # Previous Year Insights
            if 'previous_year_insights' in cf_year_data.columns:
                st.markdown(
    '<p style="color:#FFA500; font-size:22px; background-color:#444444; padding:8px; border-radius:8px; text-align:center;"><strong>📅 Previous Year Insights</strong></p>',
    unsafe_allow_html=True
)
                st.markdown("<br>", unsafe_allow_html=True)  # Adds an empty line
                st.markdown(cf_year_data['previous_year_insights'].values[0])

            # Year Comparison Insight
            if 'year_comparison_insight' in cf_year_data.columns:
                st.markdown(
    '<p style="color:#00BFFF; font-size:20px; background-color:#333333; padding:6px; border-radius:8px; text-align:center;"><strong>🔄 Year Comparison Insight</strong></p>',
    unsafe_allow_html=True
)
                st.markdown("<br>", unsafe_allow_html=True)  # Adds an empty line
                st.markdown(cf_year_data['year_comparison_insight'].values[0])

            # Patterns
            if 'patterns' in cf_year_data.columns:
                st.markdown(
    '<p style="color:#FFD700; font-size:18px; background-color:#444444; padding:4px; border-radius:8px; text-align:center;"><strong>🔍 Patterns</strong></p>',
    unsafe_allow_html=True
)
                st.markdown("<br>", unsafe_allow_html=True)  # Adds an empty line
                st.markdown(cf_year_data['patterns'].values[0])

    # Key Metrics Dashboard Tab (Tab 4)
    with tabs[4]:
        st.header("📊 Key Metrics Dashboard")
        selected_metrics = st.multiselect(
            "Select Metrics to Visualize", 
            # options=filtered_bs_data.columns, 
            options=columns_plot, 
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
