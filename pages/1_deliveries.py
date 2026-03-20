
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from dateutil.relativedelta import relativedelta

st.set_page_config(
    page_title="Deliveries",
    layout="wide",
)

"""# Logistics company dashboard"""

"""
## Statistics of deliveries for the 1st quarter
"""
f"""
### {datetime.now().strftime("%d %B %Y")}
"""
 
""

path = "data_result/"
df = pd.read_csv(path + "delivery_events_result.csv")

df = df.dropna(how="all")
df['scheduled_datetime'] = pd.to_datetime(df['scheduled_datetime'])
df['actual_datetime'] = pd.to_datetime(df['actual_datetime'])
df['on_time_flag'] = df['on_time_flag'].astype('boolean')

total_deliveries = len(df)
total_completed_delivereis = df['actual_datetime'].notna().sum()

now = datetime.now()
current_month_number = now.month
monthly_deliveries = len(df.loc[df['actual_datetime'].dt.month == current_month_number])
previous_month_date = now - relativedelta(months=1)
previous_month_number = previous_month_date.month
previous_month_deliveries = len(df.loc[df['actual_datetime'].dt.month == previous_month_number])

df2 = pd.read_csv(path + "loads_result.csv")
df2['load_date'] = pd.to_datetime(df2['load_date'])
df_monthly_deliveries = df.loc[df['actual_datetime'].dt.month == current_month_number]
df_month_loads = df2[df2['load_id'].isin(df_monthly_deliveries['load_id'])]
month_revenue = df_month_loads['revenue'].sum()

df_previous_month_deliveries = df.loc[df['actual_datetime'].dt.month == previous_month_number]
df_prvious_month_loads = df2[df2['load_id'].isin(df_previous_month_deliveries['load_id'])]
previous_month_revenue = df_prvious_month_loads['revenue'].sum()

#Number Data

with st.container(horizontal=True, gap="medium"):
    cols = st.columns(2, gap="medium", width=300)
    with cols[0]:
        st.metric(
            "Total deliveries",
            total_deliveries,
            width="content",
        )
    with cols[1]:
        st.metric(
            "Completed deliveries",
            total_completed_delivereis,
            width="content",
        )
        
    cols = st.columns(2, gap="medium", width=360)

    with cols[0]:
        st.metric(
            "Monthly deliveries",
            monthly_deliveries,
            delta=f"{monthly_deliveries - previous_month_deliveries}",
            width="content",
        )

    with cols[1]:
        st.metric(
            "Monthly revenue",
            f"{round(month_revenue)}$",
            delta=f"{round(month_revenue - previous_month_revenue)}$",
            width="content",
        )

# First Row diagrams
year = df['actual_datetime'].dropna().dt.year.unique()
months = df['actual_datetime'].dropna().dt.month.unique()
selected_months = st.pills(
    "Months to compare", months, format_func=lambda x: datetime(year[0], x, 1).strftime('%B'), default=months, selection_mode="multi"
)

if not selected_months:
    st.warning("You must select at least 1 year.", icon=":material/warning:")
    
daily = (df.groupby(df['actual_datetime'].dt.date)
         .size()
         .reset_index(name="count"))

daily['actual_datetime'] = pd.to_datetime(daily['actual_datetime'])
daily = daily[daily["actual_datetime"].dt.month.isin(selected_months)]
cols = st.columns([3, 1])

with cols[0].container(border=True, height="stretch"):
    "### Deliveries per months"

    st.altair_chart(
        alt.Chart(daily)
        .mark_bar(width=10)
        .encode(
            alt.X("actual_datetime:T", timeUnit="date").title("Date"),
            alt.Y("count:Q", title="Parcels Dispatched"),
            alt.Color("actual_datetime:N", timeUnit="month").title("Months"),
            alt.XOffset("actual_datetime:N", timeUnit="month"),
            tooltip=[
            alt.Tooltip("actual_datetime:T", title="Date", format="%Y-%m-%d"),
            alt.Tooltip("count:Q", title="Deliveries"),
        ]
        )
        .configure_legend(orient="bottom")
    )
    
delivery_status = df['actual_datetime'].notna().map({True: 'Delivered', False: 'Not Delivered'})
delivery_df = pd.DataFrame({'status': delivery_status, 'actual_datetime':df['actual_datetime']})
with cols[1].container(border=True, height="stretch"):
    "### Delivered vs undelivered shipments"

    st.altair_chart(
        alt.Chart(delivery_df)
        .mark_arc()
        .encode(
            theta="count()",
            color=alt.Color("status:N", title="Delivery Status"),
            tooltip=["status:N", "count()"]
        )
        .configure_legend(orient="bottom")
    )

#Third Row

detentions = pd.DataFrame({'detention':df['detention_minutes'], 'date':df["actual_datetime"].dt.date})
avg_detention_per_date = (detentions.groupby('date')['detention']
                         .mean()
                         .reset_index()
                         .sort_values('date'))
avg_detention_per_date.columns = ['date', 'avg_detention_minutes']


cols = st.columns([1, 3])
with cols[0].container(border=True, height="stretch"):
    avg_detention = df['detention_minutes'].mean()
    
    st.markdown("### Detention Time")
    
    st.metric(
        label="Average Detention",
        value=f"{avg_detention:.1f} minutes",
        delta=None
    )
    
    st.caption(f"Based on {df['detention_minutes'].count():,} deliveries")
with cols[1].container(border=True, height="stretch"):
    "### Detention minutes"
    st.altair_chart(
    alt.Chart(avg_detention_per_date)
    .mark_line(point=True, color='steelblue')
    .encode(
        alt.X("date:T", title="Date"),
        alt.Y("avg_detention_minutes:Q", title="Average Detention Minutes"),
        tooltip=[
            alt.Tooltip("date:T", title="Date", format="%Y-%m-%d"),
            alt.Tooltip("avg_detention_minutes:Q", title="Avg Minutes", format=".1f")
        ]
    )
    .properties(
        title="Average Detention Time by Date",
    )
    .interactive()
)