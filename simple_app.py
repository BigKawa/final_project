
import streamlit as st
import pandas as pd
import numpy as np
import functions as py  # Import the functions module
import transform as t



# This will be the input of the streamlit app User
# st input 
# bs_annual, pnl_annual, cf_annual = t.transform_pipeline(st_input)




# Testing dataframes
bs_annual = pd.read_csv("Data/bs_annual_MSFT.csv")
cf_annual = pd.read_csv("Data/cf_annual_MSFT.csv")
pnl_annual = pd.read_csv("Data/pnl_annual_MSFT.csv")

bs_annual, pnl_annual, cf_annual = t.clean_dataframes(bs_annual, pnl_annual, cf_annual)
bs_annual, pnl_annual, cf_annual = t.calculate_kpis(bs_annual, pnl_annual, cf_annual)
pnl_annual_prev, bs_annual_prev, cf_annual_prev = t.create_previous_year_dataframes(bs_annual, pnl_annual, cf_annual)
pnl_concat, bs_concat, cf_concat = t.concatenate_dataframes(bs_annual, pnl_annual, cf_annual, bs_annual_prev, pnl_annual_prev, cf_annual_prev)
pnl_concat, bs_concat, cf_concat = t.generate_insights(pnl_concat, bs_concat, cf_concat)


print(pnl_concat.info())

st.title("📊 Automated Financial Report Analysis Tool")

st.write(pnl_concat)

