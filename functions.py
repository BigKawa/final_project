import pandas as pd


# General functions for all dataframes

def cleaning(dataframe):
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
    dataframe.reset_index(drop=True, inplace=True)
    return dataframe


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

    

# pnl functions
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
    Generates enhanced financial insights for each in the income statement dataframe by comparing current and previous's data.

    Parameters
    ----------
    pnl_concated : pandas.Series
        A pnl_concated from the dataframe containing income statement data with both current and previous's columns.

    Returns
    -------
    str
        A single cohesive text containing narrative insights for the given pnl_concated.
    """
    insights = []

    # Gross Margin Insight
    if pnl_concated['grossMargin_prev'] != 0:
        gross_margin_change = ((pnl_concated['grossMargin'] - pnl_concated['grossMargin_prev']) / pnl_concated['grossMargin_prev']) * 100
        insights.append(f"In {pnl_concated['fiscalDateEnding']}, the Gross Margin was {pnl_concated['grossMargin']}% (previous year: {pnl_concated['grossMargin_prev']}%), which changed by {gross_margin_change:.2f}% compared to the previous year.")

    # Operating Margin Insight
    if pnl_concated['operatingMargin_prev'] != 0:
        operating_margin_change = ((pnl_concated['operatingMargin'] - pnl_concated['operatingMargin_prev']) / pnl_concated['operatingMargin_prev']) * 100
        insights.append(f"The Operating Margin was {pnl_concated['operatingMargin']}% (previous year: {pnl_concated['operatingMargin_prev']}%), which changed by {operating_margin_change:.2f}% compared to the previous year.")

    # Net Profit Margin Insight
    if pnl_concated['netProfitMargin_prev'] != 0:
        net_profit_margin_change = ((pnl_concated['netProfitMargin'] - pnl_concated['netProfitMargin_prev']) / pnl_concated['netProfitMargin_prev']) * 100
        insights.append(f"The Net Profit Margin was {pnl_concated['netProfitMargin']}% (previous year: {pnl_concated['netProfitMargin_prev']}%), which changed by {net_profit_margin_change:.2f}% compared to the previous year.")

    # Interest Coverage Ratio Insight
    if pnl_concated['interestCoverageRatio_prev'] != 0:
        interest_coverage_change = ((pnl_concated['interestCoverageRatio'] - pnl_concated['interestCoverageRatio_prev']) / pnl_concated['interestCoverageRatio_prev']) * 100
        insights.append(f"The Interest Coverage Ratio was {pnl_concated['interestCoverageRatio']} (previous year: {pnl_concated['interestCoverageRatio_prev']}), which changed by {interest_coverage_change:.2f}% compared to the previous year.")

    # Revenue Growth Insight
    if pnl_concated['totalRevenue_prev'] != 0:
        revenue_growth = ((pnl_concated['totalRevenue'] - pnl_concated['totalRevenue_prev']) / pnl_concated['totalRevenue_prev']) * 100
        insights.append(f"Total Revenue was {pnl_concated['totalRevenue']} (previous year: {pnl_concated['totalRevenue_prev']}), which changed by {revenue_growth:.2f}% compared to the previous year.")

    # Net Income Trends
    if pnl_concated['netIncome_prev'] != 0:
        net_income_change = ((pnl_concated['netIncome'] - pnl_concated['netIncome_prev']) / pnl_concated['netIncome_prev']) * 100
        insights.append(f"Net Income was {pnl_concated['netIncome']} (previous year: {pnl_concated['netIncome_prev']}), which changed by {net_income_change:.2f}% compared to the previous year.")

    # Operating Expenses Insight
    if pnl_concated['operatingExpenses_prev'] != 0:
        operating_expenses_change = ((pnl_concated['operatingExpenses'] - pnl_concated['operatingExpenses_prev']) / pnl_concated['operatingExpenses_prev']) * 100
        insights.append(f"Operating Expenses were {pnl_concated['operatingExpenses']} (previous year: {pnl_concated['operatingExpenses_prev']}), which changed by {operating_expenses_change:.2f}% compared to the previous year.")

    # EBITDA Insight
    if pnl_concated['ebitda_prev'] != 0:
        ebitda_change = ((pnl_concated['ebitda'] - pnl_concated['ebitda_prev']) / pnl_concated['ebitda_prev']) * 100
        insights.append(f"EBITDA was {pnl_concated['ebitda']} (previous year: {pnl_concated['ebitda_prev']}), which changed by {ebitda_change:.2f}% compared to the previous year.")

    return " ".join(insights)


def yeah_comparison_pnl(pattern_df_pnl):
    """
    Detects financial patterns in multiple metrics over multiple years and generates insights as a single string.

    Parameters
    ----------
    pattern_df_pnl : pandas.Series
        A row from the dataframe containing financial data over multiple years.

    Returns
    -------
    str
        A string providing insights about detected patterns in revenue, margins, and other financial metrics.
    """
    insights = []

    # Helper function to calculate growth
    def calculate_growth(current, previous):
        if pd.notna(previous) and previous != 0:
            return (current - previous) / previous * 100
        return None

    # Pattern 1: Growth or Decline in Revenue
    if 'totalRevenue' in pattern_df_pnl.index:
        revenue_current = pattern_df_pnl['totalRevenue']
        revenue_prev = pattern_df_pnl.get('totalRevenue_prev', None)
        growth = calculate_growth(revenue_current, revenue_prev)
        if growth is not None:
            if growth > 0:
                insights.append("Total Revenue has grown compared to the previous year, indicating strong market demand.")
            elif growth < 0:
                insights.append("Total Revenue has declined compared to the previous year, indicating potential market challenges.")

    # Pattern 2: Change in Gross Margin
    if 'grossMargin' in pattern_df_pnl.index:
        gross_margin_current = pattern_df_pnl['grossMargin']
        gross_margin_prev = pattern_df_pnl.get('grossMargin_prev', None)
        change = calculate_growth(gross_margin_current, gross_margin_prev)
        if change is not None:
            if change > 0:
                insights.append("Gross Margin has improved compared to the previous year, suggesting better cost management.")
            elif change < 0:
                insights.append("Gross Margin has decreased compared to the previous year, indicating rising production costs or pricing pressures.")

    # Pattern 3: Change in Operating Margin
    if 'operatingMargin' in pattern_df_pnl.index:
        operating_margin_current = pattern_df_pnl['operatingMargin']
        operating_margin_prev = pattern_df_pnl.get('operatingMargin_prev', None)
        change = calculate_growth(operating_margin_current, operating_margin_prev)
        if change is not None:
            if change > 0:
                insights.append("Operating Margin has increased compared to the previous year, reflecting enhanced operational efficiency.")
            elif change < 0:
                insights.append("Operating Margin has decreased compared to the previous year, indicating potential inefficiencies in operational costs.")

    # Pattern 4: Change in Net Income
    if 'netIncome' in pattern_df_pnl.index:
        net_income_current = pattern_df_pnl['netIncome']
        net_income_prev = pattern_df_pnl.get('netIncome_prev', None)
        change = calculate_growth(net_income_current, net_income_prev)
        if change is not None:
            if change > 0:
                insights.append("Net Income has grown compared to the previous year, indicating improved profitability.")
            elif change < 0:
                insights.append("Net Income has declined compared to the previous year, which may signal profitability challenges.")

    # Combine all insights into a single narrative string
    return " ".join(insights)

def generate_insights_pnl_multi_year(dataframe):
    insights_list = []
    for index, row in dataframe.iterrows():
        if index + 2 < len(dataframe):
            current_year = row['fiscalDateEnding']

            kpis = ['grossProfit', 'totalRevenue', 'costOfRevenue',
       'costofGoodsAndServicesSold', 'operatingIncome',
       'sellingGeneralAndAdministrative', 'researchAndDevelopment',
       'operatingExpenses', 'investmentIncomeNet', 'netInterestIncome',
       'interestIncome', 'interestExpense', 'nonInterestIncome',
       'otherNonOperatingIncome', 'depreciation',
       'depreciationAndAmortization', 'incomeBeforeTax', 'incomeTaxExpense',
       'interestAndDebtExpense', 'netIncomeFromContinuingOperations',
       'comprehensiveIncomeNetOfTax', 'ebit', 'ebitda', 'netIncome',
       'grossMargin', 'operatingMargin', 'netProfitMargin',
       'interestCoverageRatio']
            insights = []

            for kpi in kpis:
                current_value = row[kpi]
                next_value = dataframe.iloc[index + 1][kpi]
                next_next_value = dataframe.iloc[index + 2][kpi]

                # Analyze trends for each KPI across three years
                if current_value > next_value and next_value > next_next_value:
                    insights.append(f'The {kpi} has grown consistently over the past three years ending in {current_year}.')
                elif current_value < next_value and next_value < next_next_value:
                    insights.append(f'The {kpi} has declined consistently over the past three years ending in {current_year}.')
                elif current_value == next_value and next_value == next_next_value:
                    insights.append(f'The {kpi} has remained stable over the past three years ending in {current_year}.')
                else:
                    insights.append(f'The {kpi} has shown fluctuations over the past three years ending in {current_year}.')

            insights_list.append(' '.join(insights))
        else:
            insights_list.append('Insufficient data for trend analysis over three years.')
    return insights_list



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
    

# cashflow functions

def calculate_kpi_cf(cf_dataframe, revenue_series=None):
    """
    Calculates key performance indicators (KPIs) for a given cash flow dataframe.

    Parameters
    ----------
    cf_dataframe : pandas.DataFrame
        A dataframe containing cash flow data with columns like 'operatingCashflow', 'capitalExpenditures', 'dividendPayoutCommonStock'.
    revenue_series : pandas.Series (optional)
        A series containing revenue data for calculating cash flow margin.

    Returns
    -------
    pandas.DataFrame
        The dataframe with new columns for key cash flow metrics.
    """
    
    # Calculate Free Cash Flow (FCF)
    cf_dataframe['freeCashFlow'] = cf_dataframe['operatingCashflow'] - cf_dataframe['capitalExpenditures']
    
    # Calculate Capital Expenditure Ratio (Operating Cash Flow / Capital Expenditures)
    cf_dataframe['capitalExpenditureRatio'] = cf_dataframe['operatingCashflow'] / cf_dataframe['capitalExpenditures']
    
    # Calculate Operating Cash Flow Growth
    # Reverse the DataFrame to ensure ascending order for pct_change calculation
    cf_dataframe_reversed = cf_dataframe.iloc[::-1].copy()
    cf_dataframe_reversed['operatingCashFlowGrowth'] = cf_dataframe_reversed['operatingCashflow'].pct_change() * 100
    cf_dataframe = cf_dataframe_reversed.iloc[::-1]  # Reverse back to original order
    
    # Calculate Dividend Payout Ratio from Cash Flow
    if 'dividendPayoutCommonStock' in cf_dataframe.columns:
        cf_dataframe['dividendPayoutRatio'] = cf_dataframe['dividendPayoutCommonStock'] / cf_dataframe['operatingCashflow']
    
    # Calculate Cash Flow Margin if revenue data is provided
    if revenue_series is not None:
        cf_dataframe['cashFlowMargin'] = (cf_dataframe['operatingCashflow'] / revenue_series) * 100
    
    # Calculate Reinvestment Ratio
    cf_dataframe['reinvestmentRatio'] = cf_dataframe['capitalExpenditures'] / cf_dataframe['operatingCashflow']
    
    return cf_dataframe


def generate_cashflow_insights(df):
    """
    Analyzes key cash flow indicators from a DataFrame row and generates a cohesive narrative interpretation,
    categorizing performance into low, mid, and high classifications.

    Parameters
    ----------
    df : pandas.Series
        A row from the dataframe containing cash flow KPI metrics such as 'freeCashFlow', 'capitalExpenditureRatio',
        'operatingCashFlowGrowth', 'dividendPayoutRatio', etc.

    Returns
    -------
    str
        A single, cohesive text containing a narrative interpretation of the company's performance based on the cash flow KPI data.
    """
    insights = []

    # Free Cash Flow Insight (Classify as Low, Mid, High)
    if df['freeCashFlow'] < 0:
        insights.append(f"In {df['fiscalDateEnding']}, the company reported a **negative Free Cash Flow** of {df['freeCashFlow']}, which suggests challenges in generating enough cash to cover its capital expenditures. This could indicate potential liquidity issues.")
    elif df['freeCashFlow'] <= 5e9:
        insights.append(f"In {df['fiscalDateEnding']}, the company generated a **low Free Cash Flow** of {df['freeCashFlow']}. While still positive, this may limit the company's flexibility to reinvest in growth or return value to shareholders.")
    elif df['freeCashFlow'] <= 2e10:
        insights.append(f"In {df['fiscalDateEnding']}, the company reported a **moderate Free Cash Flow** of {df['freeCashFlow']}, indicating a balanced cash generation capability, sufficient to meet capital requirements and fund some growth initiatives.")
    else:
        insights.append(f"In {df['fiscalDateEnding']}, the company generated a **high Free Cash Flow** of {df['freeCashFlow']}, indicating strong cash generation and suggesting significant potential for expansion, dividend payouts, or debt reduction.")

    # Capital Expenditure Ratio Insight (Classify as Low, Mid, High)
    if df['capitalExpenditureRatio'] < 1:
        insights.append(f"The Capital Expenditure Ratio was **{df['capitalExpenditureRatio']:.2f}** (classified as **high**), meaning a significant portion of operating cash flow was used for capital investments. This highlights an aggressive reinvestment approach, likely focused on future growth.")
    elif df['capitalExpenditureRatio'] <= 2:
        insights.append(f"The Capital Expenditure Ratio was **{df['capitalExpenditureRatio']:.2f}** (classified as **moderate**), indicating a balanced approach to cash utilization between investment in future growth and cash retention.")
    else:
        insights.append(f"The Capital Expenditure Ratio was **{df['capitalExpenditureRatio']:.2f}** (classified as **low**), suggesting the company is retaining a substantial portion of its operating cash flow, which could imply a conservative stance toward capital reinvestment.")

    # Operating Cash Flow Growth Insight (Classify as Negative, Low, High)
    if df['operatingCashFlowGrowth'] < 0:
        insights.append(f"The Operating Cash Flow Growth was **{df['operatingCashFlowGrowth']:.2f}%**, indicating a **negative growth** compared to the previous year. This could be a warning sign of declining efficiency in generating cash from operations.")
    elif df['operatingCashFlowGrowth'] <= 10:
        insights.append(f"The Operating Cash Flow Growth was **{df['operatingCashFlowGrowth']:.2f}%**, which is classified as **low growth**. While positive, the limited growth rate may suggest challenges in improving cash generation efficiency.")
    else:
        insights.append(f"The Operating Cash Flow Growth was **{df['operatingCashFlowGrowth']:.2f}%**, classified as **high growth**, indicating significant improvement in cash generation over the past year, which reflects well on the company's operational efficiency.")

    # Dividend Payout Ratio Insight (Classify as Low, Mid, High)
    if 'dividendPayoutRatio' in df:
        if df['dividendPayoutRatio'] <= 0.25:
            insights.append(f"The Dividend Payout Ratio was **{df['dividendPayoutRatio']:.2f}** (classified as **low**), suggesting that the company retains a large portion of its cash flow for reinvestment and growth.")
        elif df['dividendPayoutRatio'] <= 0.5:
            insights.append(f"The Dividend Payout Ratio was **{df['dividendPayoutRatio']:.2f}** (classified as **moderate**), indicating a balanced strategy between rewarding shareholders and retaining cash for future opportunities.")
        else:
            insights.append(f"The Dividend Payout Ratio was **{df['dividendPayoutRatio']:.2f}** (classified as **high**), implying that the company is distributing a substantial portion of its cash flow as dividends, which may limit its ability to reinvest into growth initiatives.")

    # Reinvestment Ratio Insight (Classify as Low, Mid, High)
    if df['reinvestmentRatio'] > 0.5:
        insights.append(f"The company **reinvested** **{df['reinvestmentRatio']:.2f}** (classified as **high**) of its cash flow into its business, indicating a strong focus on expansion and growth initiatives.")
    elif df['reinvestmentRatio'] > 0.2:
        insights.append(f"The company reinvested **{df['reinvestmentRatio']:.2f}** (classified as **moderate**) of its cash flow, suggesting a balanced approach to using cash for reinvestment and other purposes.")
    else:
        insights.append(f"The company reinvested only **{df['reinvestmentRatio']:.2f}** (classified as **low**) of its cash flow, indicating a limited focus on reinvestment, potentially prioritizing cash retention or dividend payouts.")

    # Join all insights into a single narrative text
    return " ".join(insights)
