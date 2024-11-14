# 📊 Financial Analysis Automation Project

## Overview
This project automates the extraction, transformation, and analysis of financial data for public companies. The primary goal is to provide a streamlined approach for generating insights from financial statements, including the Balance Sheet, Profit & Loss (P&L) Statement, and Cash Flow Statement. The project integrates various data processing modules, with a focus on creating a user-friendly dashboard to visualize financial metrics and insights.

## **Project Description**
This **Automated Financial Report Analysis** project aims to simplify and enhance the process of analyzing financial statements by utilizing data from multiple years of financial reports. The project uses data sourced from the **Alpha Vantage API**, focusing on key financial metrics such as **Gross Margin**, **Operating Margin**, **Net Profit Margin**, and **Interest Coverage Ratio**. These KPIs are then evaluated using a rule book to generate automated insights in a narrative style, providing a comprehensive summary of the company's financial performance over time.

This project aims to automate the analysis of financial statements by using data from multiple years of reports. The data is sourced from the Alpha Vantage API, focusing on key metrics such as Gross Margin, Operating Margin, and Net Profit Margin. These metrics are evaluated to generate automated insights in a narrative style, providing a summary of the company's financial performance over time.

### **Project Goals**
- **Simplify Financial Analysis**: Automate the extraction and transformation of financial data to reduce manual effort.
- **Automated Insights**: Generate narrative insights based on predefined financial metrics to help stakeholders understand financial health at a glance.
- **Enhanced Visualization**: Provide intuitive visualizations to make data analysis accessible for non-financial professionals.
- **Problem Tackled**: This project aims to address the complexity and time-consuming nature of financial data analysis, offering automated solutions for transforming raw data into actionable insights, thereby enabling quicker decision-making for stakeholders.

## 🌟 Features
- **🔄 Data Extraction**: Uses the Alpha Vantage API to retrieve financial data for publicly listed companies. The data is saved in CSV format for further processing.
- **🔧 Data Transformation**: Transforms raw financial data into useful, structured DataFrames that can be analyzed and visualized.
- **📈 Insight Generation**: Calculates key financial ratios and provides insights based on changes between current and previous years.
- **💻 Interactive Application**: Can be integrated with a user interface such as Streamlit to provide a dynamic dashboard for stakeholders to explore financial data.

## 📂 File Descriptions

### 1. `simple_app.py`
This is the main script that ties all the components together. It:
- Retrieves financial data using the Alpha Vantage API.
- Uses the other scripts for data processing, transformation, and KPI calculations.
- Imports various libraries such as `Streamlit`, `Pandas`, `NumPy`, `Plotly`, `Seaborn`, and `Matplotlib` to facilitate user interaction and visualization.
- Currently does not contain explicitly defined functions, instead running the process flow directly.

### 2. `data_extraction_file.py`
This file is responsible for:
- **Function: `extract_financial_Data`**
  - Extracts annual financial data from the Alpha Vantage API for a given company symbol.
  - Checks if data has been previously saved in CSV format to avoid redundant API calls.
  - Transforms the data by setting 'Year' as the first column, making it easier for year-over-year analysis.
  - Returns DataFrames for balance sheet, income statement, and cash flow data.

### 3. `functions.py`
Contains reusable functions for:
- **`cleaning`**: Cleans the given DataFrame by transposing it, setting the index (`fiscalDateEnding`), and filling NaN values with zero. This is particularly useful for handling Microsoft’s income statement data.
- **`create_prev_year_old`**: Creates a new DataFrame representing the previous year's data for comparison.
- **`calculate_kpis`**: Computes key performance indicators (KPIs) for financial metrics, such as profitability and liquidity ratios.
- **`generate_balance_sheet_insights`**: Generates insights by analyzing changes in balance sheet ratios, such as the Current Ratio, Quick Ratio, and Debt-to-Equity Ratio, offering stakeholders a detailed understanding of financial health.

### 4. `transform.py`
Responsible for transforming and preparing the data, including:
- **`initialize_financial_data`**: Extracts financial data using the Alpha Vantage API and initializes it for processing.
- **`clean_dataframes`**: Cleans the financial data using the functions provided in `functions.py`.
- **`calculate_kpis`**: Calculates KPIs for the balance sheet, profit & loss statement, and cash flow statement.
- **`create_previous_year_dataframes`**: Creates DataFrames for the previous year, enabling year-over-year comparisons.
- **`concatenate_dataframes`**: Merges current and previous year DataFrames for comparative analysis.
- **`generate_insights`**: Generates narrative insights based on the changes in financial metrics.
- **`transform_pipeline`**: Orchestrates the full transformation pipeline:
  1. Initializes financial data using the API.
  2. Cleans the DataFrames.
  3. Calculates KPIs.
  4. Creates previous year DataFrames.
  5. Concatenates DataFrames.
  6. Generates financial insights.
  - Returns the concatenated DataFrames for further use in analysis or visualization.

### 5. `variables.py`
Stores important variables used throughout the project, including:
- **`columns_plot`**: A list of financial metrics and columns used in the analysis, such as `totalAssets`, `currentRatio`, `debtToEquityRatio`, `workingCapital`, etc. This helps maintain consistency and simplifies updating the metrics used across different modules.

### 6. `testing.ipynb`
This Jupyter notebook is used for:
- **🔍 Exploratory Data Analysis (EDA)**: Testing and validating different metrics such as current ratio, quick ratio, and debt-to-assets ratio.
- **📝 Insight Generation**: Providing narrative insights on financial health metrics by calculating them from the financial data.
- **🔧 Debugging**: Printing column names and data structures to ensure correctness of transformations and insights. It helps in refining and debugging the transformation methods and understanding the financial data structure.

## 🚀 Usage Instructions
1. **Setup**: Clone the repository and ensure you have Python installed with the required libraries.
2. **Install Dependencies**: Run the following command to install necessary packages:
   ```sh
   pip install -r requirements.txt
   ```
3. **Run Data Extraction**: Use `data_extraction_file.py` to pull financial data for specific companies.
4. **Data Transformation and Analysis**: Use `transform.py` and `functions.py` to process and analyze the extracted data.
5. **Run Main Application**: Execute `simple_app.py` to see the complete process in action, including API calls, data transformation, and analysis.

## 📝 Example Workflow
1. **Data Extraction**: Start by running `data_extraction_file.py` to pull financial data for a company like Apple (`AAPL`). The script will check for existing CSV files and, if necessary, call the Alpha Vantage API.
2. **Data Cleaning and Transformation**: Run `transform.py` to clean the extracted data, compute key financial ratios, and create year-over-year comparisons.
3. **Generate Insights**: The `generate_insights` function in `transform.py` will provide insights based on changes in metrics like the Current Ratio and Debt-to-Equity Ratio.
4. **Visualization**: Integrate with a tool like Streamlit to create interactive visualizations, such as trend lines for KPIs.

## 🔮 Future Work
- **User Interface**: Integrate with Streamlit or another web-based platform to create an interactive dashboard.
- **Additional Metrics**: Add more financial metrics for deeper analysis, such as advanced cash flow ratios or market-based ratios.
- **Automation**: Automate data extraction and reporting using task schedulers or cloud-based services.

## 🛠️ Requirements
- Python 3.x
- Libraries: Pandas, Requests, Streamlit, Alpha Vantage API Wrapper, etc.

## 📁 Directory Structure
```
├── simple_app.py
├── data_extraction_file.py
├── functions.py
├── transform.py
├── variables.py
├── testing.ipynb
├── README.md
├── Data/
│   └── *.csv (Extracted financial data)
└── test/
    └── *.csv (Test data files for analysis)
```

## 🤝 How to Contribute
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.

## 📜 License
This project is licensed under the MIT License.

## 📧 Contact
For any questions, feel free to contact the author or create an issue in the repository.

