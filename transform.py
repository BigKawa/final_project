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

input_symbol = "MSFT" # Test Input in this case Apple

# Initialize financial data
bs_annual, pnl_annual, cf_annual = data.extract_financial_Data(input_symbol) 

# Clean Data
bs_annual = f.cleaning(bs_annual)
cf_annual = f.cleaning(cf_annual)
pnl_annual = f.cleaning(pnl_annual)


# Calculating Kpi
cf_annual = f.calculate_kpi_cf(cf_annual)
cf_annual['insights'] = cf_annual.apply(f.generate_cashflow_insights, axis=1)


pnl_annual = f.calculating_kpi_pnl(pnl_annual)
pnl_annual["insights"] = pnl_annual.apply(f.generate_automated_insights,axis=1)


bs_annual = f.calculate_kpi_bs(bs_annual)
bs_annual["insights"] = bs_annual.apply(f.generate_insights_bs, axis=1)


# Creating a previous year file
pnl_annual_prev = f.create_prev_year(pnl_annual)
bs_annual_prev = f.create_prev_year(bs_annual)
cf_annual_prev = f.create_prev_year(cf_annual)

# Creating concatenated files
pnl_concat = pd.concat([pnl_annual,pnl_annual_prev],axis=1)
bs_concat = pd.concat([bs_annual,bs_annual_prev],axis=1)
cf_concat = pd.concat([cf_annual,cf_annual_prev],axis=1)

# Calculating Generating Insights for prev year for concatenated files
pnl_concat["previous_year_insights"] = pnl_concat.apply(f.generate_pnl_yoy_insights,axis=1)
cf_concat["previous_year_insights"] = cf_concat.apply(f.generate_cf_yoy_insights, axis=1)
bs_concat["previous_year_insights"] = bs_concat.apply(f.generate_bs_yoy_insights, axis=1)


# Creating column for yeah comparison pnl
pnl_concat["year_comparison_insight"] = pnl_concat.apply(f.yeah_comparison_pnl,axis=1)
pnl_concat["fiscalDateEnding"] = pnl_concat["fiscalDateEnding"].fillna(0).astype(int)


# Creating column for yeah comparison cf
cf_concat["year_comparison_insight"] = cf_concat.apply(f.year_comparison_cf, axis=1)


# Creating column for yeah comparison balance sheet
bs_concat["year_comparison_insight"] = bs_concat.apply(f.year_comparison_bs, axis=1)


# Generate insights for each row in the DataFrame pnl
pnl_concat["patterns"] = f.generate_insights_pnl_multi_year(pnl_concat)
# Generate insights for each row in the DataFrame cashflow
cf_concat["patterns"] = f.generate_insights_cf_multi_year(cf_concat)
# Generate insights for each row in the DataFrame balance sheet
bs_concat["patterns"] = f.generate_bs_multi_year_insights(bs_concat)

print(bs_concat)
print(cf_concat)
print(pnl_concat)