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
    dataframe = dataframe.apply(pd.to_numeric, errors='coerce').fillna(0)
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



def generate_pnl_yoy_insights(pnl_concated):
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

    # Ensure that cf_dataframe is a copy to avoid SettingWithCopyWarning
    cf_dataframe = cf_dataframe.copy()

    # Calculate Free Cash Flow (FCF)
    if 'operatingCashflow' in cf_dataframe.columns and 'capitalExpenditures' in cf_dataframe.columns:
        cf_dataframe = cf_dataframe.assign(
            freeCashFlow=cf_dataframe['operatingCashflow'] - cf_dataframe['capitalExpenditures']
        )

    # Calculate Capital Expenditure Ratio (Operating Cash Flow / Capital Expenditures)
    if 'operatingCashflow' in cf_dataframe.columns and 'capitalExpenditures' in cf_dataframe.columns:
        cf_dataframe = cf_dataframe.assign(
            capitalExpenditureRatio=cf_dataframe['operatingCashflow'] / cf_dataframe['capitalExpenditures']
        )

    # Calculate Operating Cash Flow Growth
    # Reverse the DataFrame to ensure ascending order for pct_change calculation
    if 'operatingCashflow' in cf_dataframe.columns:
        cf_dataframe_reversed = cf_dataframe.iloc[::-1].copy()
        cf_dataframe_reversed = cf_dataframe_reversed.assign(
            operatingCashFlowGrowth=cf_dataframe_reversed['operatingCashflow'].pct_change() * 100
        )
        cf_dataframe = cf_dataframe_reversed.iloc[::-1].copy()  # Reverse back to original order

    # Calculate Dividend Payout Ratio from Cash Flow
    if 'dividendPayoutCommonStock' in cf_dataframe.columns and 'operatingCashflow' in cf_dataframe.columns:
        cf_dataframe = cf_dataframe.assign(
            dividendPayoutRatio=cf_dataframe['dividendPayoutCommonStock'] / cf_dataframe['operatingCashflow']
        )

    # Calculate Cash Flow Margin if revenue data is provided
    if revenue_series is not None and 'operatingCashflow' in cf_dataframe.columns:
        cf_dataframe = cf_dataframe.assign(
            cashFlowMargin=(cf_dataframe['operatingCashflow'] / revenue_series) * 100
        )

    # Calculate Reinvestment Ratio
    if 'capitalExpenditures' in cf_dataframe.columns and 'operatingCashflow' in cf_dataframe.columns:
        cf_dataframe = cf_dataframe.assign(
            reinvestmentRatio=cf_dataframe['capitalExpenditures'] / cf_dataframe['operatingCashflow']
        )

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


def generate_cf_yoy_insights(df):
    """
    Analyzes key cash flow indicators from a DataFrame row and generates a cohesive narrative interpretation,
    comparing the current year's metrics with the previous year's metrics.

    Parameters
    ----------
    df : pandas.Series
        A row from the dataframe containing current and previous year cash flow KPI metrics such as 
        'freeCashFlow', 'capitalExpenditureRatio', 'operatingCashFlowGrowth', 'dividendPayoutRatio', 
        and their corresponding previous year columns like 'freeCashFlow_prev', 'capitalExpenditureRatio_prev', etc.

    Returns
    -------
    str
        A single, cohesive text containing a narrative interpretation of the company's year-over-year performance based on the cash flow KPI data.
    """
    yoy_insights = []

    # Free Cash Flow Year-Over-Year Insight
    if 'freeCashFlow_prev' in df:
        if df['freeCashFlow'] > df['freeCashFlow_prev']:
            yoy_insights.append(f"In {df['fiscalDateEnding']}, Free Cash Flow increased to {df['freeCashFlow']}, compared to {df['freeCashFlow_prev']} in the previous year, indicating improved cash generation efficiency.")
        elif df['freeCashFlow'] < df['freeCashFlow_prev']:
            yoy_insights.append(f"In {df['fiscalDateEnding']}, Free Cash Flow decreased to {df['freeCashFlow']}, down from {df['freeCashFlow_prev']} in the previous year, suggesting potential challenges in cash generation.")
        else:
            yoy_insights.append(f"In {df['fiscalDateEnding']}, Free Cash Flow remained consistent at {df['freeCashFlow']}, showing stability compared to the previous year.")

    # Capital Expenditure Ratio Year-Over-Year Insight
    if 'capitalExpenditureRatio_prev' in df:
        if df['capitalExpenditureRatio'] < df['capitalExpenditureRatio_prev']:
            yoy_insights.append(f"The Capital Expenditure Ratio decreased to {df['capitalExpenditureRatio']:.2f} from {df['capitalExpenditureRatio_prev']:.2f} in the previous year, indicating a more conservative investment approach.")
        elif df['capitalExpenditureRatio'] > df['capitalExpenditureRatio_prev']:
            yoy_insights.append(f"The Capital Expenditure Ratio increased to {df['capitalExpenditureRatio']:.2f}, up from {df['capitalExpenditureRatio_prev']:.2f}, suggesting increased reinvestment in growth initiatives.")
        else:
            yoy_insights.append(f"The Capital Expenditure Ratio remained steady at {df['capitalExpenditureRatio']:.2f}, showing consistency in investment approach compared to the previous year.")

    # Operating Cash Flow Growth Year-Over-Year Insight
    if 'operatingCashFlowGrowth_prev' in df:
        if df['operatingCashFlowGrowth'] > df['operatingCashFlowGrowth_prev']:
            yoy_insights.append(f"The Operating Cash Flow Growth rate improved to {df['operatingCashFlowGrowth']:.2f}% from {df['operatingCashFlowGrowth_prev']:.2f}%, highlighting enhanced efficiency in generating cash from operations.")
        elif df['operatingCashFlowGrowth'] < df['operatingCashFlowGrowth_prev']:
            yoy_insights.append(f"The Operating Cash Flow Growth rate declined to {df['operatingCashFlowGrowth']:.2f}% from {df['operatingCashFlowGrowth_prev']:.2f}%, which may indicate reduced operational efficiency.")
        else:
            yoy_insights.append(f"The Operating Cash Flow Growth rate remained unchanged at {df['operatingCashFlowGrowth']:.2f}%, showing stable performance.")

    # Dividend Payout Ratio Year-Over-Year Insight
    if 'dividendPayoutRatio_prev' in df:
        if df['dividendPayoutRatio'] > df['dividendPayoutRatio_prev']:
            yoy_insights.append(f"The Dividend Payout Ratio increased to {df['dividendPayoutRatio']:.2f}, compared to {df['dividendPayoutRatio_prev']:.2f} in the previous year, showing a greater focus on rewarding shareholders.")
        elif df['dividendPayoutRatio'] < df['dividendPayoutRatio_prev']:
            yoy_insights.append(f"The Dividend Payout Ratio decreased to {df['dividendPayoutRatio']:.2f} from {df['dividendPayoutRatio_prev']:.2f}, suggesting more cash was retained for reinvestment.")
        else:
            yoy_insights.append(f"The Dividend Payout Ratio remained stable at {df['dividendPayoutRatio']:.2f}, indicating no change in the company’s dividend policy compared to the previous year.")

    # Reinvestment Ratio Year-Over-Year Insight
    if 'reinvestmentRatio_prev' in df:
        if df['reinvestmentRatio'] > df['reinvestmentRatio_prev']:
            yoy_insights.append(f"The Reinvestment Ratio increased to {df['reinvestmentRatio']:.2f}, up from {df['reinvestmentRatio_prev']:.2f}, reflecting a stronger focus on business growth.")
        elif df['reinvestmentRatio'] < df['reinvestmentRatio_prev']:
            yoy_insights.append(f"The Reinvestment Ratio decreased to {df['reinvestmentRatio']:.2f}, down from {df['reinvestmentRatio_prev']:.2f}, indicating a reduced emphasis on reinvestment.")
        else:
            yoy_insights.append(f"The Reinvestment Ratio remained consistent at {df['reinvestmentRatio']:.2f}, showing a stable strategy toward reinvestment compared to the previous year.")

    # Join all year-over-year insights into a single narrative text
    return " ".join(yoy_insights)


# Check with previous year percentage
def year_comparison_cf(year_comparison_df):
    """
    Detects financial patterns in cash flow metrics over multiple years and generates insights as a single string.
    Use the apply function
    Parameters
    ----------
    year_comparison_df : pandas.Series
        A row from the dataframe containing cash flow data over multiple years.

    Returns
    -------
    str
        A string providing insights about detected patterns in Free Cash Flow, Capital Expenditure Ratio,
        Operating Cash Flow Growth, Dividend Payout Ratio, and Reinvestment Ratio.
    """
    insights = []

    # Helper function to calculate growth
    def calculate_growth(current, previous):
        if pd.notna(previous) and previous != 0:
            return (current - previous) / previous * 100
        return None

    # 1: Change in Free Cash Flow
    if 'freeCashFlow' in year_comparison_df.index:
        free_cash_flow_current = year_comparison_df['freeCashFlow']
        free_cash_flow_prev = year_comparison_df.get('freeCashFlow_prev', None)
        growth = calculate_growth(free_cash_flow_current, free_cash_flow_prev)
        if growth is not None:
            if growth > 0:
                insights.append(f"Free Cash Flow has increased by {growth:.2f}% compared to the previous year, indicating improved cash generation.")
            elif growth < 0:
                insights.append(f"Free Cash Flow has decreased by {abs(growth):.2f}% compared to the previous year, suggesting potential challenges in cash generation.")

    # 2: Change in Capital Expenditure Ratio
    if 'capitalExpenditureRatio' in year_comparison_df.index:
        capex_ratio_current = year_comparison_df['capitalExpenditureRatio']
        capex_ratio_prev = year_comparison_df.get('capitalExpenditureRatio_prev', None)
        change = calculate_growth(capex_ratio_current, capex_ratio_prev)
        if change is not None:
            if change > 0:
                insights.append(f"Capital Expenditure Ratio has increased by {change:.2f}% compared to the previous year, indicating a higher focus on reinvestment in growth.")
            elif change < 0:
                insights.append(f"Capital Expenditure Ratio has decreased by {abs(change):.2f}% compared to the previous year, suggesting a more conservative investment approach.")

    # 3: Change in Operating Cash Flow Growth
    if 'operatingCashFlowGrowth' in year_comparison_df.index:
        ocf_growth_current = year_comparison_df['operatingCashFlowGrowth']
        ocf_growth_prev = year_comparison_df.get('operatingCashFlowGrowth_prev', None)
        change = calculate_growth(ocf_growth_current, ocf_growth_prev)
        if change is not None:
            if change > 0:
                insights.append(f"Operating Cash Flow Growth has improved by {change:.2f}% compared to the previous year, reflecting increased operational efficiency in generating cash.")
            elif change < 0:
                insights.append(f"Operating Cash Flow Growth has decreased by {abs(change):.2f}% compared to the previous year, which may indicate a decline in cash generation efficiency.")

    # 4: Change in Dividend Payout Ratio
    if 'dividendPayoutRatio' in year_comparison_df.index:
        dividend_payout_current = year_comparison_df['dividendPayoutRatio']
        dividend_payout_prev = year_comparison_df.get('dividendPayoutRatio_prev', None)
        change = calculate_growth(dividend_payout_current, dividend_payout_prev)
        if change is not None:
            if change > 0:
                insights.append(f"Dividend Payout Ratio has increased by {change:.2f}% compared to the previous year, highlighting a stronger focus on returning value to shareholders.")
            elif change < 0:
                insights.append(f"Dividend Payout Ratio has decreased by {abs(change):.2f}% compared to the previous year, suggesting more cash is being retained for reinvestment.")

    # 5: Change in Reinvestment Ratio
    if 'reinvestmentRatio' in year_comparison_df.index:
        reinvestment_ratio_current = year_comparison_df['reinvestmentRatio']
        reinvestment_ratio_prev = year_comparison_df.get('reinvestmentRatio_prev', None)
        change = calculate_growth(reinvestment_ratio_current, reinvestment_ratio_prev)
        if change is not None:
            if change > 0:
                insights.append(f"Reinvestment Ratio has increased by {change:.2f}% compared to the previous year, indicating a stronger focus on business growth.")
            elif change < 0:
                insights.append(f"Reinvestment Ratio has decreased by {abs(change):.2f}% compared to the previous year, suggesting a reduced emphasis on reinvestment.")

    # Combine all insights into a single narrative string
    return " ".join(insights)

# Look for patterns in multiple years
def generate_insights_cf_multi_year(dataframe):
    """
    Detects financial patterns in multiple cash flow metrics over multiple years and generates insights as a list of strings.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        A dataframe containing financial data for multiple years with cash flow KPIs as columns.

    Returns
    -------
    list
        A list of strings providing insights about detected patterns in cash flow metrics like Free Cash Flow,
        Capital Expenditure Ratio, Operating Cash Flow Growth, Dividend Payout Ratio, and Reinvestment Ratio.
    """
    insights_list = []

    # List of KPIs to analyze
    kpis = ['operatingCashflow',
       'paymentsForOperatingActivities', 'proceedsFromOperatingActivities',
       'changeInOperatingLiabilities', 'changeInOperatingAssets',
       'depreciationDepletionAndAmortization', 'capitalExpenditures',
       'changeInReceivables', 'changeInInventory', 'profitLoss',
       'cashflowFromInvestment', 'cashflowFromFinancing',
       'proceedsFromRepaymentsOfShortTermDebt',
       'paymentsForRepurchaseOfCommonStock', 'paymentsForRepurchaseOfEquity',
       'paymentsForRepurchaseOfPreferredStock', 'dividendPayout',
       'dividendPayoutCommonStock', 'dividendPayoutPreferredStock',
       'proceedsFromIssuanceOfCommonStock',
       'proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet',
       'proceedsFromIssuanceOfPreferredStock',
       'proceedsFromRepurchaseOfEquity', 'proceedsFromSaleOfTreasuryStock',
       'changeInCashAndCashEquivalents', 'changeInExchangeRate', 'netIncome',
       'freeCashFlow', 'capitalExpenditureRatio', 'operatingCashFlowGrowth',
       'dividendPayoutRatio', 'reinvestmentRatio']

    for index, row in dataframe.iterrows():
        if index + 2 < len(dataframe):
            current_year = row['fiscalDateEnding']
            insights = []

            for kpi in kpis:
                current_value = row[kpi]
                next_value = dataframe.iloc[index + 1][kpi]
                next_next_value = dataframe.iloc[index + 2][kpi]

                # Analyze trends for each KPI across three years
                if current_value > next_value and next_value > next_next_value:
                    insights.append(f"The {kpi.replace('_', ' ')} has grown consistently over the past three years ending in {current_year}.")
                elif current_value < next_value and next_value < next_next_value:
                    insights.append(f"The {kpi.replace('_', ' ')} has declined consistently over the past three years ending in {current_year}.")
                elif current_value == next_value and next_value == next_next_value:
                    insights.append(f"The {kpi.replace('_', ' ')} has remained stable over the past three years ending in {current_year}.")
                else:
                    insights.append(f"The {kpi.replace('_', ' ')} has shown fluctuations over the past three years ending in {current_year}.")

            # Combine the insights for the current row into a single string
            insights_list.append(' '.join(insights))
        else:
            insights_list.append('Insufficient data for trend analysis over three years.')

    return insights_list

# balance sheet functions

def calculate_kpi_bs(bs_dataframe):
    """
    Calculate key financial metrics from the balance sheet data.

    Parameters
    ----------
    bs_dataframe : pandas.DataFrame
        DataFrame containing balance sheet data for multiple years.

    Returns
    -------
    bs_dataframe : pandas.DataFrame
        The updated DataFrame with new columns for the calculated KPIs.
    """
    # Ensure required columns exist before calculations
    available_columns = bs_dataframe.columns

    # Calculate Current Ratio
    if 'totalCurrentAssets' in available_columns and 'totalCurrentLiabilities' in available_columns:
        bs_dataframe['currentRatio'] = bs_dataframe['totalCurrentAssets'] / bs_dataframe['totalCurrentLiabilities']

    # Calculate Quick Ratio (only if inventory data is available)
    if all(col in available_columns for col in ['totalCurrentAssets', 'inventory', 'totalCurrentLiabilities']):
        bs_dataframe['quickRatio'] = (
            (bs_dataframe['totalCurrentAssets'] - bs_dataframe['inventory']) / bs_dataframe['totalCurrentLiabilities']
        )

    # Calculate Cash Ratio
    if 'cashAndCashEquivalentsAtCarryingValue' in available_columns and 'totalCurrentLiabilities' in available_columns:
        bs_dataframe['cashRatio'] = bs_dataframe['cashAndCashEquivalentsAtCarryingValue'] / bs_dataframe['totalCurrentLiabilities']

    # Calculate Debt-to-Assets Ratio
    if 'totalLiabilities' in available_columns and 'totalAssets' in available_columns:
        bs_dataframe['debtToAssetsRatio'] = bs_dataframe['totalLiabilities'] / bs_dataframe['totalAssets']

    # Calculate Debt-to-Equity Ratio
    if 'totalLiabilities' in available_columns and 'totalShareholderEquity' in available_columns:
        bs_dataframe['debtToEquityRatio'] = bs_dataframe['totalLiabilities'] / bs_dataframe['totalShareholderEquity']

    # Calculate Equity Ratio
    if 'totalShareholderEquity' in available_columns and 'totalAssets' in available_columns:
        bs_dataframe['equityRatio'] = bs_dataframe['totalShareholderEquity'] / bs_dataframe['totalAssets']

    # Calculate Working Capital
    if 'totalCurrentAssets' in available_columns and 'totalCurrentLiabilities' in available_columns:
        bs_dataframe['workingCapital'] = bs_dataframe['totalCurrentAssets'] - bs_dataframe['totalCurrentLiabilities']

    # Calculate Net Working Capital Ratio
    if 'workingCapital' in bs_dataframe.columns and 'totalAssets' in available_columns:
        bs_dataframe['netWorkingCapitalRatio'] = bs_dataframe['workingCapital'] / bs_dataframe['totalAssets']

    # Calculate Book Value per Share
    if 'totalShareholderEquity' in available_columns and 'commonStockSharesOutstanding' in available_columns:
        bs_dataframe['bookValuePerShare'] = bs_dataframe['totalShareholderEquity'] / bs_dataframe['commonStockSharesOutstanding']

    return bs_dataframe

def generate_insights_bs(df):
    """
    Generate automated insights based on the balance sheet KPIs.

    Parameters
    ----------
    df : pandas.Series
        A row from the dataframe containing balance sheet KPI metrics.

    Returns
    -------
    str
        A narrative interpretation of the company's financial position based on the KPI data.
    """
    insights = []

    # Current Ratio Insight
    if 'currentRatio' in df and pd.notna(df['currentRatio']):
        if df['currentRatio'] < 1:
            insights.append(f"In {df['fiscalDateEnding']}, the company's current ratio was {df['currentRatio']:.2f}, indicating potential liquidity concerns.")
        elif df['currentRatio'] >= 1 and df['currentRatio'] < 2:
            insights.append(f"In {df['fiscalDateEnding']}, the current ratio was {df['currentRatio']:.2f}, which suggests the company has adequate but not excessive liquidity.")
        else:
            insights.append(f"In {df['fiscalDateEnding']}, the current ratio was {df['currentRatio']:.2f}, indicating strong liquidity.")

    # Quick Ratio Insight
    if 'quickRatio' in df and pd.notna(df['quickRatio']):
        if df['quickRatio'] < 1:
            insights.append(f"The quick ratio in {df['fiscalDateEnding']} was {df['quickRatio']:.2f}, which may indicate potential challenges in covering short-term liabilities without relying on inventory.")
        else:
            insights.append(f"The quick ratio in {df['fiscalDateEnding']} was {df['quickRatio']:.2f}, indicating good short-term financial health without dependence on inventory.")

    # Cash Ratio Insight
    if 'cashRatio' in df and pd.notna(df['cashRatio']):
        if df['cashRatio'] < 0.5:
            insights.append(f"The cash ratio in {df['fiscalDateEnding']} was {df['cashRatio']:.2f}, suggesting limited cash available to cover short-term liabilities.")
        elif df['cashRatio'] >= 0.5 and df['cashRatio'] <= 1:
            insights.append(f"The cash ratio in {df['fiscalDateEnding']} was {df['cashRatio']:.2f}, indicating sufficient cash reserves to cover short-term obligations.")
        else:
            insights.append(f"The cash ratio in {df['fiscalDateEnding']} was {df['cashRatio']:.2f}, highlighting strong cash reserves.")

    # Debt-to-Assets Ratio Insight
    if 'debtToAssetsRatio' in df and pd.notna(df['debtToAssetsRatio']):
        if df['debtToAssetsRatio'] > 0.5:
            insights.append(f"The company's debt-to-assets ratio in {df['fiscalDateEnding']} was {df['debtToAssetsRatio']:.2f}, indicating a higher portion of assets financed by debt.")
        else:
            insights.append(f"The debt-to-assets ratio in {df['fiscalDateEnding']} was {df['debtToAssetsRatio']:.2f}, suggesting a lower risk of asset-based debt dependency.")

    # Debt-to-Equity Ratio Insight
    if 'debtToEquityRatio' in df and pd.notna(df['debtToEquityRatio']):
        if df['debtToEquityRatio'] > 2:
            insights.append(f"In {df['fiscalDateEnding']}, the debt-to-equity ratio was {df['debtToEquityRatio']:.2f}, indicating high leverage which may increase financial risk.")
        elif df['debtToEquityRatio'] > 1 and df['debtToEquityRatio'] <= 2:
            insights.append(f"In {df['fiscalDateEnding']}, the debt-to-equity ratio was {df['debtToEquityRatio']:.2f}, indicating moderate leverage.")
        else:
            insights.append(f"In {df['fiscalDateEnding']}, the debt-to-equity ratio was {df['debtToEquityRatio']:.2f}, indicating low leverage and potentially low risk.")

    # Equity Ratio Insight
    if 'equityRatio' in df and pd.notna(df['equityRatio']):
        if df['equityRatio'] > 0.5:
            insights.append(f"The equity ratio in {df['fiscalDateEnding']} was {df['equityRatio']:.2f}, suggesting that more than half of the company's assets are financed by equity, indicating financial stability.")
        else:
            insights.append(f"The equity ratio in {df['fiscalDateEnding']} was {df['equityRatio']:.2f}, which may indicate a higher reliance on debt financing.")

    # Working Capital Insight
    if 'workingCapital' in df and pd.notna(df['workingCapital']):
        if df['workingCapital'] < 0:
            insights.append(f"The company had negative working capital of {df['workingCapital']:.2f} in {df['fiscalDateEnding']}, indicating potential liquidity issues in meeting short-term obligations.")
        else:
            insights.append(f"The working capital in {df['fiscalDateEnding']} was {df['workingCapital']:.2f}, indicating the company's ability to cover short-term liabilities.")

    # Net Working Capital Ratio Insight
    if 'netWorkingCapitalRatio' in df and pd.notna(df['netWorkingCapitalRatio']):
        if df['netWorkingCapitalRatio'] < 0.1:
            insights.append(f"The net working capital ratio in {df['fiscalDateEnding']} was {df['netWorkingCapitalRatio']:.2f}, suggesting limited working capital relative to the company's total assets.")
        else:
            insights.append(f"The net working capital ratio in {df['fiscalDateEnding']} was {df['netWorkingCapitalRatio']:.2f}, indicating adequate working capital relative to the company's total assets.")

    # Book Value per Share Insight
    if 'bookValuePerShare' in df and pd.notna(df['bookValuePerShare']):
        insights.append(f"The book value per share in {df['fiscalDateEnding']} was {df['bookValuePerShare']:.2f}, providing an indication of the per-share equity value available to shareholders.")

    # Join all insights into a single cohesive narrative
    return " ".join(insights)


def generate_bs_yoy_insights(bs_concated):
    """
    Generates enhanced financial insights for each row in the balance sheet dataframe by comparing current and previous year's data.

    Parameters
    ----------
    bs_concated : pandas.Series
        A row from the dataframe containing balance sheet data with both current and previous year's columns.

    Returns
    -------
    str
        A single cohesive text containing narrative insights for the given bs_concated.
    """
    insights = []

    # Current Ratio Insight
    if bs_concated['currentRatio_prev'] != 0:
        current_ratio_change = ((bs_concated['currentRatio'] - bs_concated['currentRatio_prev']) / bs_concated['currentRatio_prev']) * 100
        insights.append(f"In {bs_concated['fiscalDateEnding']}, the Current Ratio was {bs_concated['currentRatio']:.2f} (previous year: {bs_concated['currentRatio_prev']:.2f}), which changed by {current_ratio_change:.2f}% compared to the previous year.")

    # Quick Ratio Insight
    if bs_concated['quickRatio_prev'] != 0:
        quick_ratio_change = ((bs_concated['quickRatio'] - bs_concated['quickRatio_prev']) / bs_concated['quickRatio_prev']) * 100
        insights.append(f"The Quick Ratio was {bs_concated['quickRatio']:.2f} (previous year: {bs_concated['quickRatio_prev']:.2f}), which changed by {quick_ratio_change:.2f}% compared to the previous year.")

    # Cash Ratio Insight
    if bs_concated['cashRatio_prev'] != 0:
        cash_ratio_change = ((bs_concated['cashRatio'] - bs_concated['cashRatio_prev']) / bs_concated['cashRatio_prev']) * 100
        insights.append(f"The Cash Ratio was {bs_concated['cashRatio']:.2f} (previous year: {bs_concated['cashRatio_prev']:.2f}), which changed by {cash_ratio_change:.2f}% compared to the previous year.")

    # Debt-to-Assets Ratio Insight
    if bs_concated['debtToAssetsRatio_prev'] != 0:
        debt_to_assets_change = ((bs_concated['debtToAssetsRatio'] - bs_concated['debtToAssetsRatio_prev']) / bs_concated['debtToAssetsRatio_prev']) * 100
        insights.append(f"The Debt-to-Assets Ratio was {bs_concated['debtToAssetsRatio']:.2f} (previous year: {bs_concated['debtToAssetsRatio_prev']:.2f}), which changed by {debt_to_assets_change:.2f}% compared to the previous year.")

    # Debt-to-Equity Ratio Insight
    if bs_concated['debtToEquityRatio_prev'] != 0:
        debt_to_equity_change = ((bs_concated['debtToEquityRatio'] - bs_concated['debtToEquityRatio_prev']) / bs_concated['debtToEquityRatio_prev']) * 100
        insights.append(f"The Debt-to-Equity Ratio was {bs_concated['debtToEquityRatio']:.2f} (previous year: {bs_concated['debtToEquityRatio_prev']:.2f}), which changed by {debt_to_equity_change:.2f}% compared to the previous year.")

    # Equity Ratio Insight
    if bs_concated['equityRatio_prev'] != 0:
        equity_ratio_change = ((bs_concated['equityRatio'] - bs_concated['equityRatio_prev']) / bs_concated['equityRatio_prev']) * 100
        insights.append(f"The Equity Ratio was {bs_concated['equityRatio']:.2f} (previous year: {bs_concated['equityRatio_prev']:.2f}), which changed by {equity_ratio_change:.2f}% compared to the previous year.")

    # Working Capital Insight
    if bs_concated['workingCapital_prev'] != 0:
        working_capital_change = ((bs_concated['workingCapital'] - bs_concated['workingCapital_prev']) / bs_concated['workingCapital_prev']) * 100
        insights.append(f"The Working Capital was {bs_concated['workingCapital']:.2f} (previous year: {bs_concated['workingCapital_prev']:.2f}), which changed by {working_capital_change:.2f}% compared to the previous year.")

    # Net Working Capital Ratio Insight
    if bs_concated['netWorkingCapitalRatio_prev'] != 0:
        net_working_capital_change = ((bs_concated['netWorkingCapitalRatio'] - bs_concated['netWorkingCapitalRatio_prev']) / bs_concated['netWorkingCapitalRatio_prev']) * 100
        insights.append(f"The Net Working Capital Ratio was {bs_concated['netWorkingCapitalRatio']:.2f} (previous year: {bs_concated['netWorkingCapitalRatio_prev']:.2f}), which changed by {net_working_capital_change:.2f}% compared to the previous year.")

    # Book Value per Share Insight
    if bs_concated['bookValuePerShare_prev'] != 0:
        book_value_change = ((bs_concated['bookValuePerShare'] - bs_concated['bookValuePerShare_prev']) / bs_concated['bookValuePerShare_prev']) * 100
        insights.append(f"The Book Value per Share was {bs_concated['bookValuePerShare']:.2f} (previous year: {bs_concated['bookValuePerShare_prev']:.2f}), which changed by {book_value_change:.2f}% compared to the previous year.")

    return " ".join(insights)


# comparison Kpi with prev year insights in percentage

def year_comparison_bs(bs_year_df):
    """
    Compares balance sheet KPIs with the previous year's data and generates narrative insights.
    
    Parameters
    ----------
    bs_year_df : pandas.Series
        A series containing balance sheet data for the current year and previous year KPIs.
    
    Returns
    -------
    str
        A narrative interpretation highlighting percentage changes in key balance sheet metrics 
        such as Current Ratio, Quick Ratio, Cash Ratio, Debt-to-Assets Ratio, Debt-to-Equity Ratio, 
        Equity Ratio, Working Capital, Net Working Capital Ratio, and Book Value per Share.
    """
    insights = []

    # Helper function to calculate growth
    def calculate_growth(current, previous):
        if pd.notna(previous) and previous != 0:
            return (current - previous) / previous * 100
        return None

    # Current Ratio Insight
    if 'currentRatio' in bs_year_df.index:
        current_ratio_current = bs_year_df['currentRatio']
        current_ratio_prev = bs_year_df.get('currentRatio_prev', None)
        growth = calculate_growth(current_ratio_current, current_ratio_prev)
        if growth is not None:
            if growth > 0:
                insights.append(f"Current Ratio has increased by {growth:.2f}% compared to the previous year, indicating improved short-term liquidity and a better ability to cover short-term obligations.")
            elif growth < 0:
                insights.append(f"Current Ratio has decreased by {abs(growth):.2f}% compared to the previous year, suggesting potential challenges in covering short-term liabilities.")
            else:
                insights.append(f"Current Ratio has remained stable compared to the previous year, indicating consistent short-term liquidity.")

    # Quick Ratio Insight
    if 'quickRatio' in bs_year_df.index:
        quick_ratio_current = bs_year_df['quickRatio']
        quick_ratio_prev = bs_year_df.get('quickRatio_prev', None)
        growth = calculate_growth(quick_ratio_current, quick_ratio_prev)
        if growth is not None:
            if growth > 0:
                insights.append(f"Quick Ratio has increased by {growth:.2f}% compared to the previous year, suggesting improved liquidity without relying on inventory.")
            elif growth < 0:
                insights.append(f"Quick Ratio has decreased by {abs(growth):.2f}% compared to the previous year, indicating potential difficulties in meeting short-term liabilities without inventory.")
            else:
                insights.append(f"Quick Ratio has remained stable compared to the previous year, indicating consistent short-term liquidity without inventory dependency.")

    # Cash Ratio Insight
    if 'cashRatio' in bs_year_df.index:
        cash_ratio_current = bs_year_df['cashRatio']
        cash_ratio_prev = bs_year_df.get('cashRatio_prev', None)
        growth = calculate_growth(cash_ratio_current, cash_ratio_prev)
        if growth is not None:
            if growth > 0:
                insights.append(f"Cash Ratio has increased by {growth:.2f}% compared to the previous year, highlighting stronger cash reserves to cover short-term liabilities.")
            elif growth < 0:
                insights.append(f"Cash Ratio has decreased by {abs(growth):.2f}% compared to the previous year, suggesting reduced cash reserves to meet short-term obligations.")
            else:
                insights.append(f"Cash Ratio has remained stable compared to the previous year, indicating consistent cash reserves.")

    # Debt-to-Assets Ratio Insight
    if 'debtToAssetsRatio' in bs_year_df.index:
        debt_to_assets_current = bs_year_df['debtToAssetsRatio']
        debt_to_assets_prev = bs_year_df.get('debtToAssetsRatio_prev', None)
        growth = calculate_growth(debt_to_assets_current, debt_to_assets_prev)
        if growth is not None:
            if growth > 0:
                insights.append(f"Debt-to-Assets Ratio has increased by {growth:.2f}% compared to the previous year, indicating a higher proportion of assets financed by debt, which may increase financial risk.")
            elif growth < 0:
                insights.append(f"Debt-to-Assets Ratio has decreased by {abs(growth):.2f}% compared to the previous year, suggesting a reduced reliance on debt for financing assets.")
            else:
                insights.append(f"Debt-to-Assets Ratio has remained stable compared to the previous year, indicating consistent debt financing levels.")

    # Debt-to-Equity Ratio Insight
    if 'debtToEquityRatio' in bs_year_df.index:
        debt_to_equity_current = bs_year_df['debtToEquityRatio']
        debt_to_equity_prev = bs_year_df.get('debtToEquityRatio_prev', None)
        growth = calculate_growth(debt_to_equity_current, debt_to_equity_prev)
        if growth is not None:
            if growth > 0:
                insights.append(f"Debt-to-Equity Ratio has increased by {growth:.2f}% compared to the previous year, reflecting higher financial leverage and increased risk for shareholders.")
            elif growth < 0:
                insights.append(f"Debt-to-Equity Ratio has decreased by {abs(growth):.2f}% compared to the previous year, indicating reduced leverage and potentially lower financial risk.")
            else:
                insights.append(f"Debt-to-Equity Ratio has remained stable compared to the previous year, indicating consistent leverage levels.")

    # Equity Ratio Insight
    if 'equityRatio' in bs_year_df.index:
        equity_ratio_current = bs_year_df['equityRatio']
        equity_ratio_prev = bs_year_df.get('equityRatio_prev', None)
        growth = calculate_growth(equity_ratio_current, equity_ratio_prev)
        if growth is not None:
            if growth > 0:
                insights.append(f"Equity Ratio has increased by {growth:.2f}% compared to the previous year, indicating a greater proportion of assets financed by shareholders' equity, which suggests financial stability.")
            elif growth < 0:
                insights.append(f"Equity Ratio has decreased by {abs(growth):.2f}% compared to the previous year, suggesting increased reliance on debt financing.")
            else:
                insights.append(f"Equity Ratio has remained stable compared to the previous year, indicating consistent equity financing levels.")

    # Working Capital Insight
    if 'workingCapital' in bs_year_df.index:
        working_capital_current = bs_year_df['workingCapital']
        working_capital_prev = bs_year_df.get('workingCapital_prev', None)
        growth = calculate_growth(working_capital_current, working_capital_prev)
        if growth is not None:
            if growth > 0:
                insights.append(f"Working Capital has increased by {growth:.2f}% compared to the previous year, showing an improved ability to meet short-term obligations.")
            elif growth < 0:
                insights.append(f"Working Capital has decreased by {abs(growth):.2f}% compared to the previous year, indicating potential liquidity issues in meeting short-term obligations.")
            else:
                insights.append(f"Working Capital has remained stable compared to the previous year, indicating consistent ability to cover short-term liabilities.")

    # Net Working Capital Ratio Insight
    if 'netWorkingCapitalRatio' in bs_year_df.index:
        net_working_capital_current = bs_year_df['netWorkingCapitalRatio']
        net_working_capital_prev = bs_year_df.get('netWorkingCapitalRatio_prev', None)
        growth = calculate_growth(net_working_capital_current, net_working_capital_prev)
        if growth is not None:
            if growth > 0:
                insights.append(f"Net Working Capital Ratio has increased by {growth:.2f}% compared to the previous year, providing a better overview of working capital relative to total assets.")
            elif growth < 0:
                insights.append(f"Net Working Capital Ratio has decreased by {abs(growth):.2f}% compared to the previous year, suggesting reduced working capital efficiency.")
            else:
                insights.append(f"Net Working Capital Ratio has remained stable compared to the previous year, indicating consistent working capital relative to total assets.")

    # Book Value per Share Insight
    if 'bookValuePerShare' in bs_year_df.index:
        book_value_current = bs_year_df['bookValuePerShare']
        book_value_prev = bs_year_df.get('bookValuePerShare_prev', None)
        growth = calculate_growth(book_value_current, book_value_prev)
        if growth is not None:
            if growth > 0:
                insights.append(f"Book Value per Share has increased by {growth:.2f}% compared to the previous year, indicating a higher per-share equity value available to shareholders.")
            elif growth < 0:
                insights.append(f"Book Value per Share has decreased by {abs(growth):.2f}% compared to the previous year, suggesting a decline in per-share equity value.")
            else:
                insights.append(f"Book Value per Share has remained stable compared to the previous year, indicating consistent per-share equity value.")

    # Combine all insights into a single narrative string
    return " ".join(insights)

# Look for Patterns
def generate_bs_multi_year_insights(dataframe):
    """
    Detects financial patterns in multiple balance sheet metrics over multiple years and generates insights as a list of strings.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        A dataframe containing financial data for multiple years with balance sheet KPIs as columns.

    Returns
    -------
    list
        A list of strings providing insights about detected patterns in balance sheet metrics like Current Ratio, Quick Ratio,
        Cash Ratio, Debt-to-Assets Ratio, Debt-to-Equity Ratio, Equity Ratio, Working Capital, Net Working Capital Ratio,
        and Book Value per Share.
    """
    insights_list = []

    # List of KPIs to analyze
    kpis = [
        'totalAssets', 'totalCurrentAssets',
       'cashAndCashEquivalentsAtCarryingValue', 'cashAndShortTermInvestments',
       'inventory', 'currentNetReceivables', 'totalNonCurrentAssets',
       'propertyPlantEquipment', 'accumulatedDepreciationAmortizationPPE',
       'intangibleAssets', 'intangibleAssetsExcludingGoodwill', 'goodwill',
       'investments', 'longTermInvestments', 'shortTermInvestments',
       'otherCurrentAssets', 'otherNonCurrentAssets', 'totalLiabilities',
       'totalCurrentLiabilities', 'currentAccountsPayable', 'deferredRevenue',
       'currentDebt', 'shortTermDebt', 'totalNonCurrentLiabilities',
       'capitalLeaseObligations', 'longTermDebt', 'currentLongTermDebt',
       'longTermDebtNoncurrent', 'shortLongTermDebtTotal',
       'otherCurrentLiabilities', 'otherNonCurrentLiabilities',
       'totalShareholderEquity', 'treasuryStock', 'retainedEarnings',
       'commonStock', 'commonStockSharesOutstanding', 'currentRatio',
       'quickRatio', 'cashRatio', 'debtToAssetsRatio', 'debtToEquityRatio',
       'equityRatio', 'workingCapital', 'netWorkingCapitalRatio',
       'bookValuePerShare'
       ]

    for index, row in dataframe.iterrows():
        if index + 2 < len(dataframe):
            current_year = row['fiscalDateEnding']
            insights = []

            for kpi in kpis:
                current_value = row[kpi]
                next_value = dataframe.iloc[index + 1][kpi]
                next_next_value = dataframe.iloc[index + 2][kpi]

                # Analyze trends for each KPI across three years
                if current_value > next_value and next_value > next_next_value:
                    insights.append(f"The {kpi.replace('_', ' ')} has grown consistently over the past three years ending in {current_year}.")
                elif current_value < next_value and next_value < next_next_value:
                    insights.append(f"The {kpi.replace('_', ' ')} has declined consistently over the past three years ending in {current_year}.")
                elif current_value == next_value and next_value == next_next_value:
                    insights.append(f"The {kpi.replace('_', ' ')} has remained stable over the past three years ending in {current_year}.")
                else:
                    insights.append(f"The {kpi.replace('_', ' ')} has shown fluctuations over the past three years ending in {current_year}.")

            # Combine the insights for the current row into a single string
            insights_list.append(' '.join(insights))
        else:
            insights_list.append('Insufficient data for trend analysis over three years.')

    return insights_list


