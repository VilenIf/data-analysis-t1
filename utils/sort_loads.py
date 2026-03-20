import streamlit as st
import pandas as pd
from datetime import datetime

path = "/data/"
result_path = "/data_result/"
df1 = pd.read_csv(path + "loads.csv")
df2 = pd.read_csv(result_path + "delivery_events_result.csv")
df = df1[df1['load_id'].isin(df2['load_id'])]
df['load_date'] = pd.to_datetime(df['load_date'])
df["load_date"] = df["load_date"] + pd.DateOffset(years=2)
print(df)  
df.to_csv(result_path+'loads_result.csv') 