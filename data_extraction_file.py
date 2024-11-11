import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
import os

api_key_2 ="JP7TLKK2YPF8I2ER"
api_key = "34KPIW7MIZGD3P5R"
api = "NYY0WO4YPAEM5C6H"


fd = FundamentalData(key= api, output_format="pandas")



# Test Input in this case Microsoft 
input = "MSFT"  # later to replace with streamlit input


def extract_financial_Data(input_symbol):
    """
    Extracts and transforms annual financial Data for a given company symbol.

    This function retrieves annual balance sheet, income statement, and cash flow Data
    for the provided input symbol using the Alpha Vantage API. It checks if the Data 
    has been previously saved as CSV files to avoid redundant API calls, and if not, 
    calls the API to fetch the Data. The Data is then transformed to have 'Year' as 
    the first column and saved as CSV files for future use.

    Parameters
    ----------
    input_symbol : str
        The stock ticker symbol of the company for which to extract financial Data.

    Returns
    -------
    tuple of pandas.DataFrame
        A tuple containing three DataFrames: `bs_annual`, `pnl_annual`, and `cf_annual`,
        which represent the annual balance sheet, income statement, and cash flow Data 
        respectively.
    """
    # Check if Data files already exist to avoid redundant API calls
    if os.path.exists(f"Data/bs_annual_{input_symbol}.csv"):
        # Load Data from CSV if it already exists
                
       bs_annual = pd.read_csv(f"Data/bs_annual_{input_symbol}.csv")
       pnl_annual = pd.read_csv(f"Data/pnl_annual_{input_symbol}.csv")
       cf_annual = pd.read_csv(f"Data/cf_annual_{input_symbol}.csv")

        
    else:
        cf_annual = fd.get_cash_flow_annual(input_symbol)[0].T
        bs_annual = fd.get_balance_sheet_annual(input_symbol)[0].T
        pnl_annual = fd.get_income_statement_annual(input_symbol)[0].T
        
     # Transforming Data
        bs_annual = bs_annual.reset_index().rename(columns={"index": "Year"}).reset_index(drop=True)
        pnl_annual = pnl_annual.reset_index().rename(columns={"index": "Year"}).reset_index(drop=True)
        cf_annual = cf_annual.reset_index().rename(columns={"index": "Year"}).reset_index(drop=True)

    
    
    # Save Data to CSV to avoid redundant calls in the future
    bs_annual.to_csv(f"Data/bs_annual_{input_symbol}.csv", index=False)
    pnl_annual.to_csv(f"Data/pnl_annual_{input_symbol}.csv", index=False)
    cf_annual.to_csv(f"Data/cf_annual_{input_symbol}.csv", index=False)

    return bs_annual, pnl_annual, cf_annual



