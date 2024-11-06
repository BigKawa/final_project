import pandas as pd

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
    # Set the first pnl_concated as the header
    dataframe.columns = dataframe.iloc[0]
    # Drop the first pnl_concated
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


def generate_insights_pnl(pnl_concated):

    """
    Generates enhanced financial insights for each year in the income statement dataframe by comparing current year and previous year's data.

    Parameters
    ----------
    pnl_concated : pandas.Series
        A pnl_concated from the dataframe containing income statement data with both current year and previous year's columns.

    Returns
    -------
    str
        A single cohesive text containing narrative insights for the given pnl_concated.
    """
    insights = []

    # Gross Margin Insight
    if pnl_concated['grossMargin_prev_year'] != 0:
        gross_margin_change = ((pnl_concated['grossMargin'] - pnl_concated['grossMargin_prev_year']) / pnl_concated['grossMargin_prev_year']) * 100
        insights.append(f"In {pnl_concated['fiscalDateEnding']}, the Gross Margin was {pnl_concated['grossMargin']}%, which changed by {gross_margin_change:.2f}% compared to the previous year.")

    # Operating Margin Insight
    if pnl_concated['operatingMargin_prev_year'] != 0:
        operating_margin_change = ((pnl_concated['operatingMargin'] - pnl_concated['operatingMargin_prev_year']) / pnl_concated['operatingMargin_prev_year']) * 100
        insights.append(f"The Operating Margin was {pnl_concated['operatingMargin']}%, which changed by {operating_margin_change:.2f}% compared to the previous year.")

    # Net Profit Margin Insight
    if pnl_concated['netProfitMargin_prev_year'] != 0:
        net_profit_margin_change = ((pnl_concated['netProfitMargin'] - pnl_concated['netProfitMargin_prev_year']) / pnl_concated['netProfitMargin_prev_year']) * 100
        insights.append(f"The Net Profit Margin was {pnl_concated['netProfitMargin']}%, which changed by {net_profit_margin_change:.2f}% compared to the previous year.")

    # Interest Coverage Ratio Insight
    if pnl_concated['interestCoverageRatio_prev_year'] != 0:
        interest_coverage_change = ((pnl_concated['interestCoverageRatio'] - pnl_concated['interestCoverageRatio_prev_year']) / pnl_concated['interestCoverageRatio_prev_year']) * 100
        insights.append(f"The Interest Coverage Ratio was {pnl_concated['interestCoverageRatio']}, which changed by {interest_coverage_change:.2f}% compared to the previous year.")

    # Revenue Gpnl_concatedth Insight
    if pnl_concated['totalRevenue_prev_year'] != 0:
        revenue_gpnl_concatedth = ((pnl_concated['totalRevenue'] - pnl_concated['totalRevenue_prev_year']) / pnl_concated['totalRevenue_prev_year']) * 100
        insights.append(f"Total Revenue was {pnl_concated['totalRevenue']}, which changed by {revenue_gpnl_concatedth:.2f}% compared to the previous year.")

    # Net Income Trends
    if pnl_concated['netIncome_prev_year'] != 0:
        net_income_change = ((pnl_concated['netIncome'] - pnl_concated['netIncome_prev_year']) / pnl_concated['netIncome_prev_year']) * 100
        insights.append(f"Net Income was {pnl_concated['netIncome']}, which changed by {net_income_change:.2f}% compared to the previous year.")

    # Operating Expenses Insight
    if pnl_concated['operatingExpenses_prev_year'] != 0:
        operating_expenses_change = ((pnl_concated['operatingExpenses'] - pnl_concated['operatingExpenses_prev_year']) / pnl_concated['operatingExpenses_prev_year']) * 100
        insights.append(f"Operating Expenses were {pnl_concated['operatingExpenses']}, which changed by {operating_expenses_change:.2f}% compared to the previous year.")

    # EBITDA Insight
    if pnl_concated['ebitda_prev_year'] != 0:
        ebitda_change = ((pnl_concated['ebitda'] - pnl_concated['ebitda_prev_year']) / pnl_concated['ebitda_prev_year']) * 100
        insights.append(f"EBITDA was {pnl_concated['ebitda']}, which changed by {ebitda_change:.2f}% compared to the previous year.")

    return " ".join(insights)



def create_prev_year(df_current_year):    
    """
    Creates a new dataframe df_prev with data from the previous year.

    Parameters
    ----------
    df_current_year : pandas.DataFrame
        A dataframe containing the current year's data for the company.

    Returns
    -------
    pandas.DataFrame
        The newly created dataframe with data from the previous year.
    """
    
    # Create a new pnl dataframe with previous year data
    df_prev = df_current_year.set_index("fiscalDateEnding").shift(-1)
    df_prev.fillna(0,inplace=True)
    df_prev = df_prev.select_dtypes(exclude=['object']).astype(int).reset_index(drop=True)
    df_prev.columns = [F"{col}_prev" for col in df_prev.columns]
    
    return df_prev