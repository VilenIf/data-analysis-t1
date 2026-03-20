
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from dateutil.relativedelta import relativedelta

deliveries = st.Page("pages/1_deliveries.py", title="Deliveries", icon=":material/delivery_truck_speed:")
locations = st.Page("pages/2_locations.py", title="Locations", icon=":material/globe_location_pin:")
raw = st.Page("pages/3_raw_data.py", title="Raw Data", icon=":material/settings:")
pg = st.navigation([deliveries, locations, raw], position="top")
pg.run()

