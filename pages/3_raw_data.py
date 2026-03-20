import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
st.set_page_config(
    page_title="Locations",
    layout="wide"
)

"""# Logistics company dashboard"""

"""
## Raw data used in project
"""
f"""
### {datetime.now().strftime("%d %B %Y")}
"""
 
""
path = "data/"
path_result = "data_result/"
df_full = pd.read_csv(path_result + "delivery_events_result.csv")
df_full_loads = pd.read_csv(path_result + "loads_result.csv")
df_full_routes = pd.read_csv(path + "routes.csv")

cols = st.columns(1)
with cols[0].container(border=True, height="stretch"):
    "### Delivery events" 
    df_full
cols = st.columns(2)
with cols[0].container(border=True, height="stretch"):
    "### Loads" 
    df_full_loads
with cols[1].container(border=True, height="stretch"):
    "### Routes" 
    df_full_routes

    