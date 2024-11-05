import pandas as pd

def first_clean(dataframe):
    """
    This function is used to clean the given dataframe by setting the index as fiscalDateEnding,
    and filling NaN values with 0. It is used to clean the balance sheet and cash flow data of
    Microsoft.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The dataframe to be cleaned.

    Returns
    -------
    pandas.DataFrame
        The cleaned dataframe.
    """
    # Set the first kpi_data as the header
    dataframe.columns = dataframe.iloc[0]  # Set the first kpi_data as column headers
    dataframe = dataframe.drop(index=dataframe.index[0])  # Drop the kpi_data that was used as column names
    dataframe = dataframe.iloc[1:]  # Drop the first kpi_data
    dataframe.set_index("fiscalDateEnding", inplace=True)  # Set the index as fiscalDateEnding

    # Convert all columns to numeric and handle NaN values
    dataframe = dataframe.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    # Transpose the dataframe
    dataframe = dataframe.T  # Transpose to make the fiscal dates columns and metrics as kpi_datas
    dataframe.index = dataframe.index.map(lambda x: int(str(x)[:4]))

    return dataframe

def second_clean(dataframe):
    """
    This function is used to clean the given dataframe by transposing it, setting the index as fiscalDateEnding,
    and filling NaN values with 0. It is used to clean the income statement data of Microsoft.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The dataframe to be cleaned.

    Returns
    -------
    pandas.DataFrame
        The cleaned dataframe.
    """
    # Transpose the dataframe and reset index
    dataframe = dataframe.T.reset_index(drop=True)
    # Set the first row as the header
    dataframe.columns = dataframe.iloc[0]
    # Drop the first row
    dataframe = dataframe[1:]
    # Shortening Dates
    dataframe["fiscalDateEnding"] = dataframe["fiscalDateEnding"].map(lambda x: int(str(x)[:4]))
    # Drop the reportedCurrency column
    dataframe = dataframe.drop(columns="reportedCurrency")
    # Convert all columns to numeric and handle NaN values
    dataframe = dataframe.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    return dataframe

def calculating_kpi_pnl(pnl_dataframe):  
    """
    Calculates key performance indicators (KPIs) for a given income statement dataframe.

    Parameters
    ----------
    pnl_dataframe : pandas.DataFrame
        A dataframe containing income statement data with columns such as 'grossProfit', 'totalRevenue',
        'operatingIncome', 'netIncome', 'ebit', and 'interestExpense'.

    Returns
    -------
    pandas.DataFrame
        The dataframe with new columns for Gross Margin, Operating Margin, Net Profit Margin, and
        Interest Coverage Ratio.
    """
    
    # Calculate Gross Margin as a percentage
    pnl_dataframe["grossMargin"] = (pnl_dataframe["grossProfit"] / pnl_dataframe["totalRevenue"]) * 100
    
    # Calculate Operating Margin as a percentage
    pnl_dataframe["operatingMargin"] = (pnl_dataframe["operatingIncome"] / pnl_dataframe["totalRevenue"]) * 100
    
    # Calculate Net Profit Margin as a percentage
    pnl_dataframe["netProfitMargin"] = (pnl_dataframe["netIncome"] / pnl_dataframe["totalRevenue"]) * 100

    # Calculate Interest Coverage Ratio
    pnl_dataframe["interestCoverageRatio"] = pnl_dataframe["ebit"] / pnl_dataframe["interestExpense"]
    
    return pnl_dataframe
    

def generate_automated_insights(kpi_data):
    """
    Generates a narrative of automated insights based on key performance indicators (KPIs) data.

    Parameters
    ----------
    kpi_data : pandas.DataFrame
        A dataframe containing KPI data with columns such as 'fiscalDateEnding', 'grossMargin',
        'operatingMargin', 'netProfitMargin', and 'interestCoverageRatio'.

    Returns
    -------
    str
        A narrative string that provides insights into the company's financial performance, focusing on
        gross margin, operating margin, net profit margin, and interest coverage ratio. The insights
        assess aspects like cost control, operational efficiency, profitability, and financial stability.
    """
    
def generate_automated_insights(df):
    
    """
    Analyzes key performance indicators (KPIs) from a df of data and generates a cohesive narrative interpretation.

    Parameters
    ----------
    df : pandas.Series
        A df from the dataframe containing KPI metrics such as 'grossMargin', 'operatingMargin',
        'netProfitMargin', and 'interestCoverageRatio'.

    Returns
    -------
    str
        A single, cohesive text containing a narrative interpretation of the company's performance based on the KPI data.
    """
    insights = []

    # Gross Margin Insight
    if df['grossMargin'] < 60:
        insights.append(f"In {df['fiscalDateEnding']}, the company had a Gross Margin of {df['grossMargin']}%, which is below industry standards. This might indicate challenges in cost control.")
    elif df['grossMargin'] > 80:
        insights.append(f"In {df['fiscalDateEnding']}, the company demonstrated an excellent Gross Margin of {df['grossMargin']}%, highlighting strong cost efficiency in production.")

    # Operating Margin Insight
    if df['operatingMargin'] < 30:
        insights.append(f"The Operating Margin was {df['operatingMargin']}%, which is quite low and suggests potential inefficiencies in managing operational costs.")
    elif df['operatingMargin'] > 50:
        insights.append(f"The Operating Margin stood at {df['operatingMargin']}%, reflecting efficient management of operational costs and a strong financial position.")

    # Net Profit Margin Insight
    if df['netProfitMargin'] < 20:
        insights.append(f"Net Profit Margin was recorded at {df['netProfitMargin']}%, signaling profitability challenges.")
    elif df['netProfitMargin'] > 35:
        insights.append(f"Net Profit Margin was an impressive {df['netProfitMargin']}%, indicating strong overall profitability.")

    # Interest Coverage Ratio Insight
    if df['interestCoverageRatio'] < 10:
        insights.append(f"The Interest Coverage Ratio was {df['interestCoverageRatio']}, suggesting some financial vulnerability when it comes to covering interest payments.")
    elif df['interestCoverageRatio'] > 15:
        insights.append(f"The Interest Coverage Ratio was healthy at {df['interestCoverageRatio']}, showing that the company has no issues covering its interest obligations.")

    # Join all insights into a single narrative text
    return " ".join(insights)
