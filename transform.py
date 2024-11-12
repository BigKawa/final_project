import pandas as pd
import functions as f
import matplotlib.pyplot as plt
import data_extraction_file as data
import os

# Windows path
# os.chdir('C:\\Users\\Nutzer\\GitHub\\Ironhack\\Groupwork\\final_project')

# checking working directory
print("Current Working Directory:", os.getcwd())
os.chdir('C:\\Users\\Nutzer\\GitHub\\Ironhack\\Groupwork\\final_project')
print("Current Working Directory:", os.getcwd())

# input_symbol = "MSFT" # Test Input in this case Apple


# Brauch ich das ? 
def initialize_financial_data(input_symbol):
    """
    Extracts and initializes financial data for the given input symbol.
    """
    bs_annual, pnl_annual, cf_annual = data.extract_financial_Data(input_symbol)
    return bs_annual, pnl_annual, cf_annual



def clean_dataframes(bs_annual, pnl_annual, cf_annual):
    """
    Cleans the financial data DataFrames using the functions module.
    """
    bs_annual = f.cleaning(bs_annual)
    pnl_annual = f.cleaning(pnl_annual)
    cf_annual = f.cleaning(cf_annual)
    return bs_annual, pnl_annual, cf_annual


def calculate_kpis(bs_annual, pnl_annual, cf_annual):
    """
    Calculates KPIs for balance sheet, profit & loss, and cash flow statements.
    """
    cf_annual = f.calculate_kpi_cf(cf_annual)
    cf_annual['insights'] = cf_annual.apply(f.generate_cashflow_insights, axis=1)

    pnl_annual = f.calculating_kpi_pnl(pnl_annual)
    pnl_annual["insights"] = pnl_annual.apply(f.generate_automated_insights, axis=1)

    bs_annual = f.calculate_kpi_bs(bs_annual)
    bs_annual["insights"] = bs_annual.apply(f.generate_insights_bs, axis=1)
    
    return bs_annual, pnl_annual, cf_annual




def create_previous_year_dataframes(bs_annual, pnl_annual, cf_annual):
    """
    Creates previous year dataframes for comparison.
    """
    pnl_annual_prev = f.create_prev_year(pnl_annual)
    bs_annual_prev = f.create_prev_year(bs_annual)
    cf_annual_prev = f.create_prev_year(cf_annual)
    
    return pnl_annual_prev, bs_annual_prev, cf_annual_prev





def concatenate_dataframes(bs_annual, pnl_annual, cf_annual, bs_annual_prev, pnl_annual_prev, cf_annual_prev):
    """
    Concatenates current and previous year dataframes for analysis.
    """
    pnl_concat = pd.concat([pnl_annual, pnl_annual_prev], axis=1)
    bs_concat = pd.concat([bs_annual, bs_annual_prev], axis=1)
    cf_concat = pd.concat([cf_annual, cf_annual_prev], axis=1)

    return pnl_concat, bs_concat, cf_concat




def generate_insights(pnl_concat, bs_concat, cf_concat):
    """
    Generates insights for concatenated DataFrames.
    """
    # Generate year-over-year insights
    pnl_concat["previous_year_insights"] = pnl_concat.apply(f.generate_pnl_yoy_insights, axis=1)
    cf_concat["previous_year_insights"] = cf_concat.apply(f.generate_cf_yoy_insights, axis=1)
    bs_concat["previous_year_insights"] = bs_concat.apply(f.generate_bs_yoy_insights, axis=1)

    # Create year comparison columns
    pnl_concat["year_comparison_insight"] = pnl_concat.apply(f.yeah_comparison_pnl, axis=1)
    pnl_concat["fiscalDateEnding"] = pnl_concat["fiscalDateEnding"].fillna(0).astype(int)
    cf_concat["year_comparison_insight"] = cf_concat.apply(f.year_comparison_cf, axis=1)
    bs_concat["year_comparison_insight"] = bs_concat.apply(f.year_comparison_bs, axis=1)

    # Generate multi-year pattern insights
    pnl_concat["patterns"] = f.generate_insights_pnl_multi_year(pnl_concat)
    cf_concat["patterns"] = f.generate_insights_cf_multi_year(cf_concat)
    bs_concat["patterns"] = f.generate_bs_multi_year_insights(bs_concat)

    return pnl_concat, bs_concat, cf_concat



def transform_pipeline(input_symbol):
    
    
    """
    A pipeline for transforming and analyzing financial data.

    This function takes a stock ticker symbol as input and returns three concatenated DataFrames: balance sheet, income statement, and cash flow.

    The pipeline consists of the following steps:

    1. Initialize financial data using the Alpha Vantage API.
    2. Clean the DataFrames using the functions module.
    3. Calculate key performance indicators (KPIs) for the financial data.
    4. Create previous year DataFrames for comparison.
    5. Concatenate current and previous year DataFrames.
    6. Generate insights for the concatenated DataFrames.

    Parameters
    ----------
    input_symbol : str
        The stock ticker symbol of the company for which to extract financial data.

    Returns
    -------
    tuple of pandas.DataFrame
        A tuple containing three DataFrames: balance sheet, income statement, and cash flow.
        in this order: bs_concat, cf_concat, pnl_concat
    """
    
    # Step 1: Initialize Financial Data
    bs_annual, pnl_annual, cf_annual = initialize_financial_data(input_symbol)

    # Step 2: Clean the DataFrames
    bs_annual, pnl_annual, cf_annual = clean_dataframes(bs_annual, pnl_annual, cf_annual)

    # Step 3: Calculate KPIs
    bs_annual, pnl_annual, cf_annual = calculate_kpis(bs_annual, pnl_annual, cf_annual)

    # Step 4: Create Previous Year DataFrames
    pnl_annual_prev, bs_annual_prev, cf_annual_prev = create_previous_year_dataframes(bs_annual, pnl_annual, cf_annual)

    # Step 5: Concatenate DataFrames
    pnl_concat, bs_concat, cf_concat = concatenate_dataframes(bs_annual, pnl_annual, cf_annual, bs_annual_prev, pnl_annual_prev, cf_annual_prev)

    # Step 6: Generate Insights
    pnl_concat, bs_concat, cf_concat = generate_insights(pnl_concat, bs_concat, cf_concat)

    # Return the transformed DataFrames
    return bs_concat, cf_concat, pnl_concat

# Test to print the concat files 
# print(bs_concat)
# print(cf_concat)
# print(pnl_concat)