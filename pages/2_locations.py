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
## Statistics of locations for the 1st quarter
"""
f"""
### {datetime.now().strftime("%d %B %Y")}
"""
 
""
path = "data/"
path_result = "data_result/"
df_full = pd.read_csv(path_result + "delivery_events_result.csv")
df_full['actual_datetime'] = pd.to_datetime(df_full['actual_datetime'])
df_full_loads = pd.read_csv(path_result + "loads_result.csv")
df_full_routes = pd.read_csv(path + "routes.csv")


df = df_full_loads
df2 = df_full_routes
df_merge = pd.merge(df, df2, on="route_id")
df_merge = df_merge[['load_id','route_id', 'typical_distance_miles', 'typical_transit_days']]

first_day = df_full['actual_datetime'].min().date()  # Simpler way
day_difference = datetime.now().date() - first_day
day_difference = day_difference.days

delivered_shipments = len(df_full.loc[df_full['actual_datetime'].notna()])

with st.container(horizontal=True, gap="medium"):
    cols = st.columns(2, gap="medium", width=400)
    with cols[0]:
        st.metric(
            "Total miles driven",
            df_merge['typical_distance_miles'].sum(),
            width="content",
        )
    with cols[1]:
        st.metric(
            "Miles per day",
            round(df_merge['typical_distance_miles'].sum() / day_difference),
            width="content",)
    cols = st.columns(2, gap="medium", width=400) 
    with cols[0]:
        st.metric(
            "Total days in transit",
            df_merge['typical_transit_days'].sum(),
            width="content",
        )
    with cols[1]:
        st.metric(
            "Shipments per day",
            round(delivered_shipments / day_difference),
            width="content",
        )

    # with cols[1]:
    #     st.metric(
    #         "Monthly revenue",
    #         f"{round(month_revenue)}$",
    #         width="content",
    #     )
        
df = df_full['location_city'].value_counts().head(5).reset_index()
cols = st.columns(2)
with cols[0].container(border=True, height="stretch"):
    "### Our top destinations"
    
    st.altair_chart(
    alt.Chart(df)
    .mark_bar()
    .encode(
        alt.X("location_city:N", title="City", sort='-x'),  # Remove timeUnit
        alt.Y("count:Q", title="# of deliveries"),
        alt.Color("count:Q", 
                  title="Deliveries",
                  scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=["location_city:N", "count:Q"],
    ).properties(
        height=400
    )   
)
df = df_full['location_state'].value_counts().reset_index()
with cols[1].container(border=True, height="stretch"):
    "### Deliveries by states"
    st.altair_chart(
        alt.Chart(df)
        .mark_arc()
        .encode(
            theta="count",
            color=alt.Color("location_state:N", title="US state", scale=alt.Scale(scheme='blues')),
            tooltip=["location_state:N", "count"]
        )
        .configure_legend(orient="bottom")
    )
